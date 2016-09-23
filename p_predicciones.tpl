% include('header_predicciones.tpl', title='Predicciones', ndd=noticias_del_dia)
	<h1>Predicciones del nivel de alérgenos por municipio</h1>
	<p>Seleccione un municipio para visualizar la predicción del nivel de brote alérgico de gramíneas para los próximos 3 días.</p>
	<form action="/prediccion_muni" method="post" enctype="multipart/form-data">
		<table border="1" class="centro">
		<colgroup>
			<col />
		</colgroup>
		<tr>
			<td class="centrotd">
				<select name="municipio">
				% for m in muni:
				<option value="{{m.attrib["value"][-5:]}}-{{m.text}}">{{m.text}}</option>
				%end
				</select>
			</td>
		</tr>
		<tr>
			<td class="boton">
				<input value="Ver Predicción" type="submit" onclick="toggle('spinner');"/>
				<img src="/static/style/spinner.gif" id="spinner" style="display: none;" alt=""/>
			</td>
		</tr>
		</table>
	</form>	
	<table class="blanco">
		<tr>
		<td class="fondo"> 
			<table border="1">
				<colgroup>
					<col />
					<col />
				</colgroup>
				<thead>
					<tr>
						<th scope="col" colspan="2" align="center">Municipios con mayor nivel de alerta para el día: <b>{{listaStrings[0]}}</b></th>
					</tr>
				</thead>
				<tbody>				
				% for p in listaPredicciones[0]:
					<tr>
						<th scope="row">{{p['MunicipioOrig']}}</th>
						<td>{{p[listaStrings[1]]}}</td>
					</tr>
				% end
				</tbody> 			
			</table>
		</td>
		<td  class="fondo"> 
		  <img src="data:image/png;base64, {{plot_url}}" alt="" id="municipio-cam" />
		</td>
		</tr>
	</table>
	<table class="blanco">
		<tr>
		<td class="fondo"> 
			<table border="1">
				<colgroup>
					<col />
					<col />
				</colgroup>
				<thead>
					<tr>
						<th scope="col" colspan="2" align="center">Municipios con mayor nivel de alerta para el día: <b>{{listaStrings[2]}}</b> </th>
					</tr>
				</thead>
				<tbody>
				% for p in listaPredicciones[1]:
					<tr>
						<th scope="row">{{p['MunicipioOrig']}}</th>
						<td>{{p[listaStrings[3]]}}</td>
					</tr>
				% end
				</tbody> 
			</table>
		</td>
		<td class="fondo"> 
			<table border="1">
				<colgroup>
					<col />
					<col />
				</colgroup>
				<thead>
					<tr>
						<th scope="col" colspan="2" align="center">Municipios con mayor nivel de alerta para el día: <b>{{listaStrings[4]}}</b> </th>
					</tr>
				</thead>
				<tbody>
				% for p in listaPredicciones[2]:
					<tr>
						<th scope="row">{{p['MunicipioOrig']}}</th>
						<td>{{p[listaStrings[5]]}}</td>
					</tr>
				% end
				</tbody> 			

			</table>		
		</td>
		</tr>
	</table>

% include('footer.tpl')
