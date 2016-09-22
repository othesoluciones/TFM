% include('header_reporte.tpl', title='¡Repórtanos!', ndd=noticias_del_dia)
<h1>Repórtanos alertas</h1>
<p>Si quieres ayudarnos a mejorar nuestra predicción, puedes hacerlo si nos reportas una alerta del municipio en el que te encuentres.</p>
% if alta==1:
 <p id="idverde"><b>Alerta recibida con éxito. Gracias por su colaboración</b></p>
% end
<form action="/reporta" method="post">
<table border="1">

        <colgroup>
           <col />
           <col />
        </colgroup>


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
             <th scope="row">Nivel</th>
             <td>
				<select name="nivel_de_alerta">
					<option value="ninguno" selected="selected">Seleccione un nivel de alerta</option>
					% for n in nivel:
						<option value="{{n.attrib["value"][-5:]}}">{{n.text}}</option>
					%end
				</select>
			 </td>
           </tr>
        </tbody>
		<tbody>
           <tr>
             <th scope="row"></th>
             <td>
             	<input value="Reportar alerta" type="submit" onclick="toggle('spinner');"/>
             	<img src="/static/style/spinner.gif" id="spinner" style="display: none;" alt=""/>
             </td>
           </tr>
        </tbody>
		
 </table>
</form>	
<p>Alertas notificadas por nuestros usuarios durante el día <b>{{hoy}}</b>:</p>
	<table border="1">

        <colgroup>
           <col />
           <col />
           <col />
        </colgroup>

        <thead>
           <tr>
             <th scope="col">Municipio</th>
             <th scope="col">Nivel de Alerta Reportada</th>
			 <th scope="col">Hora</th>
           </tr>
        </thead>

		%for colRep in coleccion_reportes:
        <tbody>
			<tr>
				<td>
					{{colRep['municipio_label']}}
				</td>
				<td>
					{{colRep['labelAlerta']}}
				</td>
				<td>
					{{colRep['hora']}}
				</td>
			</tr>
		</tbody>
		%end
 </table>
	<div>
      %if prev_page is not None:
      <a href="/reporte/{{prev_page}}">&lt; Prev</a>
      %end
      %if next_page is not None:
      <a href="/reporte/{{next_page}}">Next &gt;</a>
      %end
    </div>
% include('footer.tpl')
