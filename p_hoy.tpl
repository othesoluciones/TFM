% include('header_hoy.tpl', title='Niveles del día', ndd=noticias_del_dia)
	<h1>Municipios de Madrid</h1>
	<table>
		<tr>
		<td width="33%"  id="idblanco" valign="top"> 
		<table border="1" valign="top">
			<colgroup>
				<col />
			</colgroup>
			<thead>
			<tr>
				<th scope="col">Zona1</th>
			</tr>
			</thead>
			<tbody valign="top">
				<tr>
					<td>
						<ul>
						% for i in range(0,len(listaZona1[0])):
							<li><a href={{listaZona1[0][i]}}>{{listaZona1[1][i]}}</a></li>
						%end
						</ul>
					</td>
				</tr>
			</tbody>
		</table>
		</td>
		<td width="67%"  id="idblanco" valign="top"> 
		  <img src="data:image/png;base64, {{plot_url}}" alt="" id="municipio-cam" />
		</td>
		</tr>
	</table>	
	
	<table border="1" valign="top">

        <colgroup>
           <col />
           <col />
        </colgroup>

        <thead>
           <tr>
             <th scope="col">Zona2</th>
             <th scope="col">Zona4</th>
			 <th scope="col">Zona6</th>
           </tr>
        </thead>


        <tbody valign="top">
			<tr>
				<td>
					<ul>
						% for i in range(0,len(listaZona2[0])):
							<li><a href={{listaZona2[0][i]}}>{{listaZona2[1][i]}}</a></li>
						%end
					</ul>
				</td>
				<td>
					<ul>
						% for i in range(0,len(listaZona4[0])):
							<li><a href={{listaZona4[0][i]}}>{{listaZona4[1][i]}}</a></li>
						%end
					</ul>
				</td>
				<td>
					<ul>
						% for i in range(0,len(listaZona6[0])):
							<li><a href={{listaZona6[0][i]}}>{{listaZona6[1][i]}}</a></li>
						%end
					</ul>
				</td>
			</tr>
		</tbody>
        <thead align="center">
           <tr>
             <th scope="col">Zona3</th>
             <th scope="col">Zona5</th>
			 <th scope="col">Zona7</th>
           </tr>
        </thead>
        <tbody valign="top">
			<tr>
				<td>
					<ul>
						% for i in range(0,len(listaZona3[0])):
							<li><a href={{listaZona3[0][i]}}>{{listaZona3[1][i]}}</a></li>
						%end
					</ul>
				</td>
				<td>
					<ul>
						% for i in range(0,len(listaZona5[0])):
							<li><a href={{listaZona5[0][i]}}>{{listaZona5[1][i]}}</a></li>
						%end
					</ul>
				</td>
				<td>
					<ul>
						% for i in range(0,len(listaZona7[0])):
							<li><a href={{listaZona7[0][i]}}>{{listaZona7[1][i]}}</a></li>
						%end
					</ul>
				</td>
			</tr>
		</tbody>
	</table>
% include('footer.tpl')
