% include('header_reporte.tpl', title='¡Repórtanos!')
<h1>Repórtanos alertas</h1>
<h2 id="idrojo">Por favor, seleccione un municipio correcto</h2>
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
					<option value="ninguno" >Seleccione un nivel de alerta</option>
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


% include('footer.tpl')