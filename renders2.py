'''Librerias necesarias para el proyecto'''
from wsgiref.validate import validator
from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask import flash
import psycopg2
from conectar import conectar
from wtforms import DateField, Form, StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired
from datetime import datetime, timedelta
import os

'''La primera linea crea una isntancia de la clase Flask
La segunda configura una clave secreta para la aplicacion,
Esto sirve para firmar cookies y otras cosas relacionadas con la seguridad.'''
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

'''Render formulario de registro'''
class SignInForm(FlaskForm):
    Nickname=StringField('Nickname', validators=[validators.DataRequired()])
    Nombre=StringField('Nombre', validators=[validators.DataRequired()])
    Apellidos=StringField('Apellidos',validators=[validators.DataRequired()])
    Correo=StringField('Correo', validators=[validators.DataRequired()])
    Contrasena=PasswordField('Contrasena', validators=[validators.DataRequired()]) 
    submit=SubmitField('Registrar')


'''Render Formulario de ingreso'''
class LoginForm(FlaskForm):
    Correo=StringField('Correo', validators=[DataRequired()])
    Contrasena=PasswordField('Contrasena', validators=[DataRequired()])
    submit=SubmitField('Iniciar Sesion')


'''Render formulario creacion grupo
class CreargrupoForm(FlaskForm):
    Nombre_grupo=StringField('Nombre_Grupo', validators=[validators.DataRequired()])
    ID_administrador=StringField('ID_administrador',validators=[validators.DataRequired()])
    '''

'''La primeria linea crea una instancia de la clase LoginManager el cual ayudara a gestionar las sesiones
La segunda linea incializa el objeto en la aplicacion'''
login_manager = LoginManager()
login_manager.init_app(app)

'''La primera linea define una clase usuario '''
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

'''La segunda linea define una funscion load_user 
como argumento y devuelve una instancia de la clase
 User'''
def load_user(user_id):
    return User(user_id)

'''Registra la funcion load_user como la funcion 
para cargar a un usuario'''
login_manager.user_loader(load_user)

#inicio de renders para las paginas que existen
#html's dentro de templates: inicio
@app.route('/')
def Home():
    return render_template("Home.html", url_for=url_for)

@app.route('/Signin')
def Signin():
    form=SignInForm()
    return render_template("Signin.html",form=form)

@app.route('/Login')
def Login():
    form=LoginForm()
    return render_template("Login.html",form=form)

@app.route('/startPage')
@login_required
def startPage():
    user_id=current_user.id
    '''
    racha_pagos_a_tiempo=obtener_racha_pagos_a_tiempo(user_id)
    pagos_pendientes=obtener_pagos_pendientes(user_id)
    pagos_completados=obtener_pagos_completados(user_id)
    print("Pagos completados del mes: ",pagos_completados)

    cantidad_pagada=cantidad_pagada,
    racha_pagos_a_tiempo=racha_pagos_a_tiempo,
    pagos_pendientes=pagos_pendientes,
    pagos_completados=pagos_completados
    '''
    return render_template(
        "startPage.html",
        url_for=url_for
        )

#aqui terminan las paginas principales

#renders para paginas de grupos
#html's dentro de htmlsGrupos
class CreargrupoForm(FlaskForm):
    Nombre_grupo = StringField('Nombre_Grupo', validators=[validators.DataRequired()])
    Descripción = StringField('Descripción', validators=[validators.DataRequired()])
    Contrasena = PasswordField('Contrasena', validators=[validators.DataRequired()])
    submit = SubmitField('Crear Grupo')
#Este html es el designado para la opcion Crear Grupo
@app.route('/htmlsGrupos/grupoFormCreate', methods=['GET', 'POST'])
@login_required
def grupoFormCreate():
    form = CreargrupoForm()
    if form.validate_on_submit() and request.method=='POST':
        Nombre_grupo = form.Nombre_grupo.data
        Descripción = form.Descripción.data
        Contrasena = form.Contrasena.data

        # Obtén el ID del usuario actual
        id_usuario_actual = current_user.id

        conn = conectar()
        cur = conn.cursor()
        try:
            # Modifica la consulta para incluir el ID del usuario actual como ID_administrador
            cur.execute('INSERT INTO "Grupos" ("Nombre_grupo", "ID_administrador", "Descripción", "Contrasena") VALUES (%s, %s, %s, %s);', (Nombre_grupo, id_usuario_actual, Descripción, Contrasena))
            conn.commit()
            flash('Grupo creado exitosamente', 'success')
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            # Maneja el error según tus necesidades
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return redirect(url_for('gruposView'))
    else:
        return render_template("htmlsGrupos/grupoFormCreate.html", form=form)

#Este Html es el designado para que los usuarios puedan ingresar a un grupo
class JoinGrupoForm(FlaskForm):
    IdGrupo = StringField('ID del Grupo', validators=[DataRequired()])
    ContrasenaGrupo = PasswordField('Contraseña del Grupo', validators=[DataRequired()])
    submit = SubmitField('Unirse al Grupo')
@app.route('/htmlsGrupos/grupoFormJoin', methods=['GET', 'POST'])
@login_required
def grupoFormJoin():
    form = JoinGrupoForm()

    if form.validate_on_submit():
        IdGrupo = form.IdGrupo.data
        ContrasenaGrupo = form.ContrasenaGrupo.data

        conn = conectar()
        cur = conn.cursor()
        fecha_actual = datetime.now()

        try:
            # Verifica si el grupo existe y la contraseña es correcta
            cur.execute('SELECT * FROM public."Grupos" WHERE "ID_grupo" = %s AND "Contrasena" = %s;', (IdGrupo, ContrasenaGrupo))
            grupo_info = cur.fetchone()

            if grupo_info:
                # Asigna el usuario actual como miembro del grupo
                cur.execute('''
                    INSERT INTO public."Pertenece" ("ID_usr", "ID_gru", "Fecha", "Administra")
                    VALUES (%s, %s, %s, %s);
                ''', (current_user.id, IdGrupo, fecha_actual, False))
                conn.commit()
                flash('Te uniste al grupo.', 'success')
                return redirect(url_for('gruposPertenece'))
            else:
                print('error')
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    return render_template("htmlsGrupos/grupoFormJoin.html", form=form, url_for=url_for)

@app.route('/htmlsGrupos/gruposView')
@login_required
def gruposView():
    user_id = current_user.id  # Asegúrate de tener la ID del usuario actual

    conn = conectar()
    cur = conn.cursor()

    try:
        # Consulta para obtener información de todos los grupos del usuario actual
        cur.execute('''
            SELECT "Nombre_grupo","ID_administrador", "Descripción", "Contrasena", "ID_grupo"
            FROM public."Grupos"
            WHERE "ID_administrador" = %s;
        ''', (user_id,))
        grupos_info = cur.fetchall()
        print("Grupos obtenidos:", grupos_info)
        if not grupos_info:
            print("No se encontraron grupos para el usuario.")
            return render_template("htmlsGrupos/gruposView.html", grupos_info=None)
        return render_template("htmlsGrupos/gruposView.html", grupos_info=grupos_info)

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        # Maneja el error según tus necesidades
        return render_template("htmlsGrupos/gruposView.html", grupos_info=None)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

@app.route('/gruposPertenece')
@login_required
def gruposPertenece():
    conn = conectar()
    cur = conn.cursor()

    try:
        # Obtener los grupos a los que pertenece el usuario actual
        cur.execute('''
            SELECT G."Nombre_grupo", G."ID_grupo"
            FROM public."Grupos" G
            JOIN public."Pertenece" P ON G."ID_grupo" = P."ID_gru"
            WHERE P."ID_usr" = %s;
        ''', (current_user.id,))
        grupos_pertenecientes = cur.fetchall()
        return render_template("/htmlsGrupos/gruposPertenece.html", grupos_pertenecientes=grupos_pertenecientes)

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


class EditargrupoForm(FlaskForm):
    Nombre_grupo = StringField('Nombre_Grupo', validators=[validators.DataRequired()])
    Descripción = StringField('Descripción', validators=[validators.DataRequired()])
    Contrasena = PasswordField('Contrasena', validators=[validators.DataRequired()])
    submit = SubmitField('Editar Grupo')
@app.route('/htmlsGrupos/editarGrupo/<int:grupo_id>', methods=['GET', 'POST'])
@login_required
def editarGrupo(grupo_id):
    form = EditargrupoForm()
    id_usuario_actual = current_user.id
    conn = conectar()
    cur = conn.cursor()

    try:
        # Obtener información actual del grupo
        cur.execute('SELECT "Nombre_grupo", "Descripción", "Contrasena" FROM public."Grupos" WHERE "ID_grupo" = %s;', (grupo_id,))
        grupo_info = cur.fetchone()

        # Llenar el formulario con la información actual del grupo
        form.Nombre_grupo.data = grupo_info[0]
        form.Descripción.data = grupo_info[1]
        # Puedes decidir si quieres llenar o no el campo de contraseña, dependiendo de tus necesidades
        if form.validate_on_submit():
            # Actualizar la información del grupo en la base de datos
            cur.execute('''
                UPDATE public."Grupos"
                SET "Nombre_grupo" = %s, "ID_administrador" = %s, "Descripción" = %s, "Contrasena" = %s
                WHERE "ID_grupo" = %s;
            ''', (form.Nombre_grupo.data, id_usuario_actual, form.Descripción.data, form.Contrasena.data, grupo_id))
            conn.commit()
            return redirect(url_for('gruposView'))

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return render_template("/htmlsGrupos/gruposEditar.html", form=form, grupo_id=grupo_id)

@app.route('/eliminar_grupo/<int:grupo_id>', methods=['POST'])
@login_required
def eliminar_grupo(grupo_id):
    conn = conectar()
    cur = conn.cursor()

    try:
        # Antes de eliminar el grupo, también debes eliminar las referencias en la tabla "Usuarios" y "Pertenece"
        # Aquí se asume que hay una relación en cascada configurada en la base de datos que eliminará las referencias en la tabla "Usuarios" y "Pertenece"
        cur.execute('DELETE FROM public."Grupos" WHERE "ID_grupo" = %s;', (grupo_id,))
        conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return redirect(url_for('gruposView'))

@app.route('/ver_miembros/<int:grupo_id>')
@login_required
def ver_miembros(grupo_id):
    conn = conectar()
    cur = conn.cursor()

    try:
        # Obtener la lista de miembros del grupo
        cur.execute('''
            SELECT "Nombre" FROM public."Usuarios"
            WHERE "ID_usuario" IN (
                SELECT "ID_usr" FROM public."Pertenece"
                WHERE "ID_gru" = %s
            );
        ''', (grupo_id,))

        miembros = cur.fetchall()

        return render_template("/htmlsGrupos/ver_miembros.html", grupo_id=grupo_id, miembros=miembros)

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return render_template("/htmlsGrupos/ver_miembros.html", grupo_id=grupo_id, miembros=miembros)

@app.route('/ver_pagos/<int:grupo_id>')
@login_required
def ver_pagos(grupo_id):
    conn = conectar()
    cur = conn.cursor()

    try:
        id_usuario_actual = current_user.id
        # Obtener la lista de pagos del grupo
        cur.execute('''
            SELECT "ID_pago", "Nombre_pago", "Fecha_creacion", "Estatus_pago", "ID_usuario"
            FROM public."Pagos"
            WHERE "ID_grupo" = %s AND "ID_usuario" = %s;
        ''', (grupo_id, id_usuario_actual))

        pagos = cur.fetchall()

        return render_template("ver_pagos.html", grupo_id=grupo_id, pagos=pagos)

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return render_template("/htmlsGrupos/ver_pagos.html", grupo_id=grupo_id, pagos=pagos)

@app.route('/verPago/<int:grupo_id>')
@login_required
def verPago(grupo_id):
    conn = conectar()
    cur = conn.cursor()

    try:
        id_usuario_actual = current_user.id
        # Obtener la lista de pagos del grupo
        cur.execute('''
            SELECT p."ID_pago", p."Nombre_pago", p."Fecha_creacion", p."Estatus_pago",
                   u."ID_usuario", u."Nombre"
            FROM public."Pagos" p
            INNER JOIN public."Usuarios" u ON p."ID_usuario" = u."ID_usuario"
            WHERE p."ID_grupo" = %s;
        ''', (grupo_id,))

        pagos = cur.fetchall()

        return render_template("ver_pagos.html", grupo_id=grupo_id, pagos=pagos)

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return render_template("/htmlsGrupos/verPago.html", grupo_id=grupo_id, pagos=pagos)
#aqui terminan las cosas de grupos

#Renders de paginas de pagos
#Html's dentro de htmlsPagos
class PagoFormCreate(FlaskForm):
    Nombre_pago = StringField('Nombre del Pago', validators=[DataRequired()])
    Fecha_pago = DateField('Fecha del pago', validators=[DataRequired()])
    submit = SubmitField('Unirse al Grupo')

@app.route('/htmlsGrupos/pagoFormCreate/<int:grupo_id>', methods=['GET', 'POST'])
@login_required
def pagoFormCreate(grupo_id):
    conn = conectar()
    cur = conn.cursor()
    form = PagoFormCreate(request.form)

    try:
        # Obtener información adicional sobre el grupo si es necesario
        cur.execute('SELECT "Nombre_grupo", "ID_administrador", "Descripción" FROM public."Grupos" WHERE "ID_grupo" = %s;', (grupo_id,))
        grupo_info = cur.fetchone()

        if not grupo_info:
            return redirect(url_for('gruposView'))

        if request.method == 'POST' and form.validate():
            fecha_creacion = datetime.today().strftime('%Y-%m-%d')
            fecha_pago = form.Fecha_pago.data
            nombre_pago = form.Nombre_pago.data

            # Obtener miembros del grupo
            cur.execute('SELECT "ID_usr" FROM public."Pertenece" WHERE "ID_gru" = %s;', (grupo_id,))
            miembros = cur.fetchall()

            # Lista para almacenar IDs de usuario
            ids_usuario = []

            # Insertar un registro de pago por cada miembro del grupo
            for miembro in miembros:
                id_usuario = miembro[0]
                ids_usuario.append(id_usuario)
                cur.execute('INSERT INTO public."Pagos" ("ID_grupo", "ID_usuario", "Nombre_pago", "Fecha_creacion", "Fecha_pago", "Estatus_pago") VALUES (%s, %s, %s, %s, %s, %s);', (grupo_id, id_usuario, nombre_pago, fecha_creacion, fecha_pago, False))

            conn.commit()
            flash('Pago asignado.', 'success')
            return redirect(url_for('gruposView'))

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        flash('Hubo un error al crear el pago', 'error')  # Agregar un mensaje flash de error

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    # Redirección independientemente de si hay un error o no
    return render_template("/htmlsGrupos/pagoFormCreate.html", grupo_id=grupo_id, grupo_info=grupo_info, form=form)

@app.route('/pagar/<int:grupo_id>/<int:pago_id>', methods=['POST'])
@login_required
def pagar(grupo_id, pago_id):
    # Lógica para cambiar el estado de Estatus_pago a verdadero
    conn = conectar()
    cur = conn.cursor()

    try:
        cur.execute('''
            UPDATE public."Pagos"
            SET "Estatus_pago" = TRUE
            WHERE "ID_pago" = %s;
        ''', (pago_id,))

        conn.commit()

        flash('Pago realizado con éxito', 'success')

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        flash('Hubo un error al realizar el pago', 'error')

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return redirect(url_for('ver_pagos', grupo_id=grupo_id))
# Método para obtener la racha de pagos a tiempo del usuario
def obtener_racha_pagos_a_tiempo(user_id):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT 
                "ID_pago",
                "Nombre_pago",
                "Fecha_creacion",
                "Fecha_pago",
                "Estatus_pago",
                CASE
                    WHEN "Cantidad_a_pagar" = 0 AND "Fecha_limite" <= "Fecha_pago" THEN 'Completado'
                    WHEN "Fecha_pago" <= "Fecha_limite" THEN 'A tiempo'
                    ELSE 'Atrasado'
                END AS "Estado_pago"
            FROM
                public."Pagos"
            WHERE
                "ID_usuario" = %s
        ''', (user_id,))
        pagos = cur.fetchall()

        racha_actual = 0
        max_racha = 0
        racha_pagos_a_tiempo = []

        for pago in pagos:
            estado_pago = pago[4]  # La columna "Estatus_pago"

            if estado_pago == 'A tiempo' or estado_pago == 'Completado':
                racha_actual += 1
                racha_pagos_a_tiempo.append(pago)
            else:
                max_racha = max(max_racha, racha_actual)
                racha_actual = 0

        # Considera el caso donde la racha continúa hasta el final
        max_racha = max(max_racha, racha_actual)

        return racha_pagos_a_tiempo
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        # Maneja el error según tus necesidades
        return []
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


# Método para obtener la suma de los pagos pendientes del usuario en el mes actual
def obtener_pagos_pendientes(user_id):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT COALESCE(SUM("Cantidad_a_pagar"), 0) as total_pendiente
            FROM public."Pagos"
            WHERE "ID_usuario" = %s
            AND "Estatus_pago" = false
            AND EXTRACT(MONTH FROM "Fecha_pago") = EXTRACT(MONTH FROM CURRENT_DATE);
        ''', (user_id,))
        total_pendiente = cur.fetchone()[0]
        return total_pendiente if total_pendiente else 0

    finally:
        cur.close()
        conn.close()

# Método para obtener la suma de los pagos completados del usuario en el mes actual
def obtener_pagos_completados(user_id):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT COUNT("ID_pago") as total_completado
            FROM public."Pagos"
            WHERE "ID_usuario" = %s
            AND "Estatus_pago" = true
            AND "Cantidad_a_pagar" = 0
            AND "Fecha_pago" <= "Fecha_limite"
            AND EXTRACT(MONTH FROM "Fecha_pago") = EXTRACT(MONTH FROM CURRENT_DATE);
        ''', (user_id,))
        total_completado = cur.fetchone()[0]
        return total_completado if total_completado else 0

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        # Maneja el error según tus necesidades
        return 0

    finally:
        cur.close()
        conn.close()


#Render para el formulario de registro
@app.route('/SignIn', methods=['POST'])
def SignIn():
    form=SignInForm()
    if form.validate_on_submit() and request.method=='POST':
        Nickname=form.Nickname.data
        Nombre=form.Nombre.data
        Apellidos=form.Apellidos.data
        Correo=form.Correo.data
        Contrasena=form.Contrasena.data
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO "Usuarios" ("Nickname", "Nombre", "Apellidos", "Correo", "Contrasena") VALUES (%s, %s, %s, %s, %s);', (Nickname, Nombre, Apellidos, Correo, Contrasena))
            conn.commit()
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            # Maneja el error según tus necesidades
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return render_template("Home.html")
    else:
        return render_template("SignIn.html", form=form)


#Render para el formulario de ingreso
@app.route("/LogIn", methods=['POST'])
def LogIn():
    logout_user()
    form=LoginForm()
    if form.validate_on_submit and request.method=='POST':
        Correo=form.Correo.data
        Contrasena=form.Contrasena.data
        print(Correo, ' ', Contrasena)
        no_match = "El correo y/o la contraseña son incorrectos"
        cur = None
        try:
            conn = conectar()
            cur=conn.cursor()
            cur.execute('SELECT "Correo", "Contrasena", "ID_usuario" FROM "Usuarios" WHERE "Correo" = %s AND "Contrasena" = %s;', (Correo, Contrasena))
            r = cur.fetchall()
            if len(r) == 0:
                print('1')
                raise Exception(no_match)
            else:
                print('0')
                print(r[0][0], ' ', r[0][1], ' ', r[0][2])
                user_id = r[0][2]
                user = User(user_id)
                login_user(user)
        except (psycopg2.DatabaseError, Exception) as error:
            print(type(error))
            if str(error)==no_match:
                print('1')
                return redirect(url_for('Login'))
            print(error)   
            print('0')
        finally:
            if cur is not None:
                cur.close()
                if conn is not None:
                    conn.close()
                    return redirect(url_for('startPage'))
    else:
        return render_template("Login.html")
    
@app.route('/Logout')
def Logout():
    logout_user()

    # Redireccionar al usuario a la página de inicio de sesión
    return redirect(url_for('Login'))

'''es una construccion comun en python
se utiliza para asegurarse de que el servdor flask
solo se ejecute si el script python se esta ejecutando 
directamente y no si se esta importando de un modulo de
 otro script'''
if __name__ == '__main__':
    app.run(debug=True)