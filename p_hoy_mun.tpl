% include('header_hoy.tpl', title='Niveles del día')
    <h1>{{name}}</h1>
		<img src="data:image/png;base64, {{plot_url}}">
		% for b in busquedaAEMET:
		<table border="1">
			<caption><h2>Datos Meteorológicos</h2></caption>
			<colgroup>
				<col />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope="row">Temperatura máxima (ºC)</th>
					<td></td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Temperatura mínima (ºC)</th>
					<td>{{b['Temperatura maxima']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Humedad máxima</th>
					<td></td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Humedad mínima</th>
					<td></td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">% Precipitaciones</th>
					<td></td>
				</tr>
			</tbody> 
			<tbody>
			<tr>
				<th scope="row">Velocidad del Viento</th>
				<td></td>
           </tr>
        </tbody>
	     % end
 </table>
 		<table border="1">
			<caption><h2>Datos Calidad del Aire</h2></caption>
			<colgroup>
				<col />
				<col />
			</colgroup>
			<tbody>
				<tr>
					<th scope="row">CO</th>
					<td></td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">HO</th>
					<td></td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">HO2</th>
					<td></td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Hidrocarburos</th>
					<td></td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Ozono</th>
					<td></td>
				</tr>
			</tbody> 
 </table>
		<a href="../hoy">Volver</a>
% include('footer.tpl')