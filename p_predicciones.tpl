% include('header_predicciones.tpl', title='Predicciones', ndd=noticias_del_dia)
	<h1>Predicciones del nivel de alérgenos por municipio</h1>
	<p>Seleccione un municipio para visualizar la predicción del nivel de brote alérgico de gramíneas para los próximos 3 días.</p>
	<table>
		<td>
        <form action="/prediccion_muni" method="post" enctype="multipart/form-data">
			<table border="1">
				<colgroup>
					<col />
					<col />
				</colgroup>
				<tbody>
					<tr>
						<td colspan="2" >
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
						<td colspan="2" >
							<input value="Ver Predicción" type="submit" onclick="toggle('spinner');"/>
							<img src="/static/style/spinner.gif" id="spinner" style="display: none;" alt=""/>
						</td>
					</tr>
				</tbody>
			</table>
		</form>
		</td>
		</tr>
		<tr>
		<td> 
			<table border="1">
				<thead>
					<tr>
						<th scope="col" colspan="2" align="center">Municipios con mayor nivel de alerta para el día: <b>{{listaStrings[0]}}</b></th>
					</tr>
				</thead>
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
		</td>
		<td> 
		  <img src="data:image/png;base64, {{plot_url}}" alt="" id="municipio-cam" />
		</td>
		</tr>
	</table>
	<table>
		<tr>
		<td> 
			<table border="1">
				<thead>
					<tr>
						<th scope="col" colspan="2" align="center">Municipios con mayor nivel de alerta para el día: <b>{{listaStrings[2]}}</b> </th>
					</tr>
				</thead>
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
		</td>
		<td> 
			<table border="1">
				<thead>
					<tr>
						<th>Municipios con mayor nivel de alerta para el día: <b>{{listaStrings[4]}}</b> </th>
					</tr>
				</thead>
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
		</td>
		</tr>
	</table>

% include('footer.tpl')
