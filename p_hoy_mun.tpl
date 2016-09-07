% include('header_hoy.tpl', title='Niveles del día')
    <h1>{{name}}</h1>
		<img src="data:image/png;base64, {{plot_url}}">
		<table border="0" width="100%" cellpadding="5" cellspacing="5">
		<tr>
		<td width="50%"> 
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
					<td>{{b['Temperatura minima']}}</td>
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
					<th scope="row">Humedad relativa máxima</th>
					<td>{{b['Humedad relativa maxima']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">Humedad relativa mínima</th>
					<td>{{b['Humedad relativa minima']}}</td>
				</tr>
			</tbody> 
			<tbody>
				<tr>
					<th scope="row">% Precipitaciones</th>
					<td>{{b['precipitaciones 00-24']}}</td>
				</tr>
			</tbody> 
			<tbody>
			<tr>
				<th scope="row">Velocidad del Viento</th>
				<td>{{b['viento 00-24']}}</td>
           </tr>
        </tbody>
	     % end
 </table>
 </td>
<td width="50%"> 
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
 </td>
</tr>
</table>

		<a href="../hoy">Volver</a>
% include('footer.tpl')
