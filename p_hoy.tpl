% include('header_hoy.tpl', title='Niveles del día')
	<h1>Municipios de Madrid</h1>
	<ul>
	% for m in muni:
		<li><a href="/{{m.attrib["value"][-5:]}}/{{m.text}}">{{m.text}}</a></li>
	%end
	</ul>
	
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

		%for calAir in calidad_aire:
        <tbody>
			<tr>
				<td>
					{{calAir['Estacion']}}
				</td>
				<td>
					{{calAir['TEMPERATURA']}}
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
