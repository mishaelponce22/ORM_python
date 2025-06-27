from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from tkinter import *
from tkinter import messagebox, ttk

Base = declarative_base()

estudiante_curso = Table(
    'estudiante_curso', Base.metadata,
    Column('estudiante_id', Integer, ForeignKey('estudiantes.id')),
    Column('curso_id', Integer, ForeignKey('cursos.id')),
)

class Estudiante(Base):
    __tablename__ = 'estudiantes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    grado = Column(String(50))
    seccion = Column(String(10))
    edad = Column(Integer)
    cursos = relationship('Curso', secondary=estudiante_curso, back_populates='estudiantes')

class Curso(Base):
    __tablename__ = 'cursos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    estudiantes = relationship('Estudiante', secondary=estudiante_curso, back_populates='cursos')


engine = create_engine('postgresql+psycopg2://USUARIO:CONTRASEÑA@localhost:5432/ormdb')


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def actualizar_treeview():
    for item in tree.get_children():
        tree.delete(item)
    estudiantes = session.query(Estudiante).all()
    for e in estudiantes:
        cursos_nombres = ', '.join([c.nombre for c in e.cursos])
        tree.insert("", END, values=(e.id, e.nombre, e.grado, e.seccion, e.edad, cursos_nombres))

def actualizar_estudiante():
    id_ = entry_id.get()
    if not id_.isdigit():
        messagebox.showerror("Error", "ID inválido")
        return

    est = session.get(Estudiante, int(id_))
    if not est:
        messagebox.showerror("Error", "Estudiante no encontrado")
        return

    est.nombre = entry_nombre.get()
    est.grado = entry_grado.get()
    est.seccion = entry_seccion.get()
    est.edad = int(entry_edad.get()) if entry_edad.get().isdigit() else None

    # Actualiza cursos
    curso_nombre = combo_curso.get()
    if curso_nombre:
        curso = session.query(Curso).filter_by(nombre=curso_nombre).first()
        if curso and curso not in est.cursos:
            est.cursos.append(curso)

    session.commit()
    limpiar_campos()
    actualizar_treeview()

def insertar_estudiante():
    nombre = entry_nombre.get()
    grado = entry_grado.get()
    seccion = entry_seccion.get()
    edad = entry_edad.get()
    curso_nombre = combo_curso.get()
    if not nombre or not edad.isdigit():
        messagebox.showerror("Error", "Datos inválidos")
        return
    estudiante = Estudiante(nombre=nombre, grado=grado, seccion=seccion, edad=int(edad))
    if curso_nombre:
        curso = session.query(Curso).filter_by(nombre=curso_nombre).first()
        if curso:
            estudiante.cursos.append(curso)
    session.add(estudiante)
    session.commit()
    limpiar_campos()
    actualizar_treeview()

def eliminar_estudiante():
    id_ = entry_id.get()
    if not id_.isdigit():
        messagebox.showerror("Error", "ID inválido")
        return
    est = session.get(Estudiante, int(id_))
    if est:
        session.delete(est)
        session.commit()
        limpiar_campos()
        actualizar_treeview()

def seleccionar_item(event):
    seleccionado = tree.focus()
    if seleccionado:
        valores = tree.item(seleccionado, "values")
        entry_id.config(state=NORMAL)
        entry_id.delete(0, END)
        entry_id.insert(0, valores[0])
        entry_id.config(state=DISABLED)
        entry_nombre.delete(0, END)
        entry_nombre.insert(0, valores[1])
        entry_grado.delete(0, END)
        entry_grado.insert(0, valores[2])
        entry_seccion.delete(0, END)
        entry_seccion.insert(0, valores[3])
        entry_edad.delete(0, END)
        entry_edad.insert(0, valores[4])
        combo_curso.set("")

def limpiar_campos():
    entry_id.config(state=NORMAL)
    entry_id.delete(0, END)
    entry_id.config(state=DISABLED)
    entry_nombre.delete(0, END)
    entry_grado.delete(0, END)
    entry_seccion.delete(0, END)
    entry_edad.delete(0, END)
    combo_curso.set("")

root = Tk()
root.title("Gestión de Estudiantes y Cursos")
root.geometry("800x500")

frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="ID").grid(row=0, column=0)
entry_id = Entry(frame, state=DISABLED)
entry_id.grid(row=0, column=1)

Label(frame, text="Nombre").grid(row=1, column=0)
entry_nombre = Entry(frame)
entry_nombre.grid(row=1, column=1)

Label(frame, text="Grado").grid(row=2, column=0)
entry_grado = Entry(frame)
entry_grado.grid(row=2, column=1)

Label(frame, text="Sección").grid(row=3, column=0)
entry_seccion = Entry(frame)
entry_seccion.grid(row=3, column=1)

Label(frame, text="Edad").grid(row=4, column=0)
entry_edad = Entry(frame)
entry_edad.grid(row=4, column=1)

Label(frame, text="Curso").grid(row=5, column=0)
combo_curso = ttk.Combobox(frame, values=[c.nombre for c in session.query(Curso).all()])
combo_curso.grid(row=5, column=1)

Button(frame, text="Insertar", command=insertar_estudiante).grid(row=6, column=0, pady=5)
Button(frame, text="Eliminar", command=eliminar_estudiante).grid(row=6, column=1, pady=5)
Button(frame, text="Actualizar", command=actualizar_estudiante).grid(row=6, column=2, pady=5)


cols = ("ID", "Nombre", "Grado", "Sección", "Edad", "Cursos")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor=CENTER)
tree.pack(fill=BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", seleccionar_item)

actualizar_treeview()
root.mainloop()
