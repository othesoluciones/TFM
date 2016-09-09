% include('header_notificaciones.tpl', title='Notificaciones')
<h1>Recibe notificaciones</h1>
% if alta==1:
 <h2 id="idverde">Alerta recibida con éxito. Gracias por su colaboración</h2>
% end
<form action="/notifica" method="post" enctype="multipart/form-data">
	<table border="1">
        <colgroup>
           <col />
           <col />
        </colgroup>


        <tbody>
           <tr>
             <th scope="row">Email</th>
             <td><input name="email" type="text" /></td>
           </tr>
        </tbody> 
        <tbody>
           <tr>
             <th scope="row">Municipio</th>
             <td>
				<select name="municipio">
					<option value="ninguno" selected="selected">Seleccione un municipio</option>
					% for m in muni:
						<option value="{{m.attrib["value"][-5:]}}">{{m.text}}</option>
					%end
				</select>
			 </td>
           </tr>
        </tbody> 
        <tbody>
           <tr>
             <th scope="row">Periodicidad</th>
             <td>
				<input type="radio" name="periodicidad" value="d" id ="d" checked="checked" /><label for="d">Diaria</label><br/><br/>
				<input type="radio" name="periodicidad" value="r"/><input type="text" name="fechahora"/>
			  </td>
           </tr>
        </tbody>
		<tbody>
           <tr>
             <th scope="row"></th>
             <td>
				<input value="Realizar suscripción" type="submit" onclick="toggle('spinner');"/>
				<img src="/static/style/spinner.gif" id="spinner" style="display: none;" alt=""/>
			</td>
           </tr>
        </tbody>
	</table>
 </form>
	<h2>Notificaciones Guardadas</h2>
    <table id="notificaciones_guardadas">
    %for notif in coleccion_notificaciones:
      <tr>
        <td>
          {{notif['email']}}
        </td>
        <td>
          {{notif['captador']}}
        </td>
        <td>
          {{notif['periodicidad']}}
        </td>
		<td>
          {{notif['realizada'].strftime('%X %d %b %y')}}
        </td>
      </tr>
    %end
    </table>
	<div>
      %if prev_page is not None:
      <a href="/notificaciones/{{prev_page}}">&lt; Prev</a>
      %end
      %if next_page is not None:
      <a href="/notificaciones/{{next_page}}">Next &gt;</a>
      %end
    </div>
% include('footer.tpl')
