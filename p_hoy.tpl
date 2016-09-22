% include('header_hoy.tpl', title='Niveles del día', ndd=noticias_del_dia)
	<h1>Municipios de Madrid</h1>
	<p>Seleccione un municipio de la Comunidad de Madrid para visualizar sus datos meteorológicos y de calidad del aire correspondientes al día de <b>{{hoy}}</b></p>
	<img src="data:image/png;base64, {{plot_url}}" alt="" id="municipio-cam" />
	<img src="data:image/png;base64, {{plot_url_ley}}" alt="" id="municipio" />
	<table border="1" valign="top">

        <colgroup>
           <col />
           <col />
           <col />
        </colgroup>
	<tbody>
		<tr>
			<th scope="col">Madrid Capital</th>
			<td colspan="2">
			<br></br>
				<ul>
				% for i in range(0,len(listaZona1[0])):
					<li><a href="{{listaZona1[0][i]}}">{{listaZona1[1][i]}}</a></li>
				%end
				</ul>
			</td>			
		</tr>
           <tr>
             <th scope="col">Corredor del Henares</th>
             <th scope="col">Zona Noroeste</th>
			 <th scope="col">Cuenca del Alberche</th>
           </tr>

			<tr>
				<td>
					<ul>
						% for i in range(0,len(listaZona2[0])):
							<li><a href="{{listaZona2[0][i]}}">{{listaZona2[1][i]}}</a></li>
						%end
					</ul>
				</td>
				<td>
					<ul>
						% for i in range(0,len(listaZona4[0])):
							<li><a href="{{listaZona4[0][i]}}">{{listaZona4[1][i]}}</a></li>
						%end
					</ul>
				</td>
				<td>
					<ul>
						% for i in range(0,len(listaZona6[0])):
							<li><a href="{{listaZona6[0][i]}}">{{listaZona6[1][i]}}</a></li>
						%end
					</ul>
				</td>
			</tr>

           <tr>
             <th scope="col">Zona Sur</th>
             <th scope="col">Zona Sierra Norte</th>
			 <th scope="col">Cuenca del Tajuña</th>
           </tr>

			<tr>
				<td>
					<ul>
						% for i in range(0,len(listaZona3[0])):
							<li><a href="{{listaZona3[0][i]}}">{{listaZona3[1][i]}}</a></li>
						%end
					</ul>
				</td>
				<td>
					<ul>
						% for i in range(0,len(listaZona5[0])):
							<li><a href="{{listaZona5[0][i]}}">{{listaZona5[1][i]}}</a></li>
						%end
					</ul>
				</td>
				<td>
					<ul>
						% for i in range(0,len(listaZona7[0])):
							<li><a href="{{listaZona7[0][i]}}">{{listaZona7[1][i]}}</a></li>
						%end
					</ul>
				</td>
			</tr>
		</tbody>
	</table>
% include('footer.tpl')
