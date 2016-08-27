% include('header_hoy.tpl', title='Niveles del día')
	<h1>Predicción del día</h1>

	
	<table border="1">

        <colgroup>
           <col />
           <col />
           <col />
        </colgroup>

        <thead>
           <tr>
             <th scope="col">ESTACION</th>
             <th scope="col">TEMPERATURA EN ESTACION</th>
			 <th scope="col">DÍA</th>
			 <th scope="col">HORA</th>
           </tr>
        </thead>

		%for calAir in calidad_aire_23082016_I:
        <tbody>
			<tr>
				<td>
					{{calAir['Estacion']}}
				</td>
				<td>
					{{calAir['Temperatura']}}
				</td>
				<td>
					{{calAir['Dia']}}
				</td>
				<td>
					{{calAir['Hora']}}
				</td>
			</tr>
		</tbody>
		%end
 </table>
	<div>
      %if prev_page is not None:
      <a href="/hoy/{{prev_page}}">&lt; Prev</a>
      %end
      %if next_page is not None:
      <a href="/hoy/{{next_page}}">Next &gt;</a>
      %end
    </div>
% include('footer.tpl')