% include('header_notificaciones.tpl', title='Notificaciones', ndd=noticias_del_dia)
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
<label for="fechaDesde">Fecha desde:
 <input type="text" name="fechaDesde" id="fechaDesde" value={{fdesde}} readonly/>
</label><br/><br/>
<label for="fechaHasta">Fecha Hasta:
 <input type="text" name="fechaHasta" id="fechaHasta" value={{fhasta}} readonly/>
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

% include('footer.tpl')
