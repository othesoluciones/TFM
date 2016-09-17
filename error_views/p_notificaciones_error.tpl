% include('header_notificaciones.tpl', title='Notificaciones', ndd=noticias_del_dia)
<h1>Recibe notificaciones</h1>
% if errores[0]==False:
 <h2 id="idrojo">Por favor, introduzca una dirección de correo electrónico correcta</h2>
% end
% if errores[1]==False:
 <h2 id="idrojo">Por favor, seleccione un municipio correcto</h2>
% end
% if errores[2]==False:
 <h2 id="idrojo">Por favor, rellene ambas fechas</h2>
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
             <td><input name="email" type="text" value="{{mailSel}}" /></td>
           </tr>
        </tbody> 
        <tbody>
           <tr>
             <th scope="row">Municipio</th>
             <td>
				<select name="municipio">
					<option value="ninguno" {{!'selected="selected"' if munsel == 'ninguno' else ""}}>Seleccione un municipio</option>
					% for m in muni:
						<option value="{{m.attrib["value"][-5:]}}" {{!'selected="selected"' if munsel == m.attrib['value'][-5:] else ""}}>{{m.text}}</option>
					%end
				</select>
			 </td>
           </tr>
        </tbody> 
        <tbody>
           <tr>
            <th scope="row">Periodicidad</th>
             <td>
<label for="fechaDesde">Fecha desde:
 <input type="text" name="fechaDesde" id="fechaDesde" value="{{fdesde}}" readonly/>
</label><br/><br/>
<label for="fechaHasta">Fecha Hasta:
 <input type="text" name="fechaHasta" id="fechaHasta" value="{{fhasta}}" readonly/>
</label>
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
          {{notif['municipio']}}
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
