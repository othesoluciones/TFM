% include('header_predicciones.tpl', title='Predicciones', ndd=noticias_del_dia)
	<h1>Predicción del Nivel de Gramíneas</h1>

	<img src="data:image/png;base64, {{plot_url}}" alt="" id="municipio-cam" />
	
<table border="1">
		<caption><h2>TOP 5 Municipios con mayor nivel de gramíneas para el día<b>{{listaStrings[0]}}</b> </h2></caption>
		% for p in listaPredicciones[0]:
			<colgroup>
				<col />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope="row">{{p['Municipio']}}</th>
					<td>{{p[listaStrings[1]]}}</td>
				</tr>
			</tbody> 
			
	     % end
 </table>
 <table border="1">
		<caption><h2>TOP 5 Municipios con mayor nivel de gramíneas para el día<b>{{listaStrings[2]}}</b> </h2></caption>
		% for p in listaPredicciones[1]:
			<colgroup>
				<col />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope="row">{{p['Municipio']}}</th>
					<td>{{p[listaStrings[3]]}}</td>
				</tr>
			</tbody> 
			
	     % end
 </table>
 <table border="1">
		<caption><h2>TOP 5 Municipios con mayor nivel de gramíneas para el día<b>{{listaStrings[4]}}</b> </h2></caption>
		% for p in listaPredicciones[2]:
			<colgroup>
				<col />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope="row">{{p['Municipio']}}</th>
					<td>{{p[listaStrings[5]]}}</td>
				</tr>
			</tbody> 
			
	     % end
 </table>
<h2>Por favor seleccione el municipio del que desee visualizar la predicción del nivel de gramíneas para los próximos 3 días</h2>
 <form action="/prediccion_muni" method="post" enctype="multipart/form-data">
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
					% for m in muni:
						<option value="{{m.attrib["value"][-5:]}}-{{m.text}}">{{m.text}}</option>
					%end
				</select>
			 </td>
           </tr>
        </tbody> 
		<tbody>
           <tr>
             <th scope="row"></th>
             <td>
				<input value="Ver Predicción" type="submit" onclick="toggle('spinner');"/>
				<img src="/static/style/spinner.gif" id="spinner" style="display: none;" alt=""/>
			</td>
           </tr>
        </tbody>
	</table>
 </form>
% include('footer.tpl')
