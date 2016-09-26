% include('header_reporte.tpl', title='¡Repórtanos!', ndd=noticias_del_dia)
<h1>Repórtanos alertas</h1>
<p>Si quieres ayudarnos a mejorar nuestra predicción, puedes hacerlo si nos reportas una alerta del municipio en el que te encuentres.</b></p>
% if errores[0]==False:
<p id="idrojo"><b>Por favor, seleccione un municipio correcto</b></p>
% end
% if errores[1]==False:
<p id="idrojo"><b>Por favor seleccione un nivel correcto</b></p>
% end

<table border="1">
	<form action="/reporta" method="post">


        <colgroup>
           <col />
           <col />
        </colgroup>


        <tbody>
           <tr>
             <th scope="row">Municipio</th>
             <td>
				<select name="municipio">
					<option value="ninguno" {{!'selected="selected"' if munsel == 'ninguno' else ""}} >Seleccione un municipio</option>
					% for m in muni:
						<option value="{{m.attrib["value"][-5:]}}" {{!'selected="selected"' if munsel == m.attrib['value'][-5:] else ""}}>{{m.text}}</option>
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
					<option value="ninguno" {{!'selected="selected"' if nivsel == 'ninguno' else ""}}>Seleccione un nivel de alerta</option>
					%for n in nivel:
					      <option value="{{n.attrib["value"][-5:]}}" {{!'selected="selected"' if nivsel == n.attrib['value'] else ""}}>{{n.text}}</option>
					%end
				</select>
			 </td>
           </tr>
        </tbody>
		<tbody>
           <tr>
             <th scope="row"></th>
             <td><input value="Reportar alerta" type="submit" /></td>
           </tr>
        </tbody>
	</form>			
 </table>
% if cuantosReportes==0:
<p>No existen alertas notificadas por nuestros usuarios durante el día <b>{{hoy}}</b></p>
% end
% if cuantosReportes >=1:
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
 %end
	<div>
      %if prev_page is not None:
      <a href="/reporte/{{prev_page}}">&lt; Prev</a>
      %end
      %if next_page is not None:
      <a href="/reporte/{{next_page}}">Next &gt;</a>
      %end
    </div>

% include('footer.tpl')
