% include('header_notificaciones.tpl', title='Notificaciones')
<h1>Recibe notificaciones</h1>
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
             <th scope="row">Captador</th>
             <td><input name="captador" type="text" /></td>
           </tr>
        </tbody>
        <tbody>
           <tr>
             <th scope="row">Periodicidad</th>
             <td><input name="periodicidad" type="text" /></td>
           </tr>
        </tbody>
		<tbody>
           <tr>
             <th scope="row"></th>
             <td>
				<input value="Realizar suscripción" type="submit" onclick="toggle('spinner');/>
				<img src="/static/style/spinner.gif" id="spinner" style="display: none;">
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