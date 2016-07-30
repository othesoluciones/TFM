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
             <th scope="col">ESTACIÓN</th>
             <th scope="col">NIVEL GRAMÍNEAS</th>
             <th scope="col">OTROS</th>
           </tr>
        </thead>


        <tbody>
           <tr>
             <th scope="row">Moncloa</th>
             <td>Muuuuchas</td>
             <td>Sol</td>
           </tr>
        </tbody> 
        <tbody>
           <tr>
             <th scope="row">Arganda del rey</th>
             <td>Pocas</td>
             <td>Lluvia</td>
           </tr>
        </tbody>
 </table>

% include('footer.tpl')