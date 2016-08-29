% include('header_predicciones.tpl', title='Predicciones')
	<h1>Predicciones futuras</h1>

	<img src="data:image/png;base64, {{plot_url}}">
	
	<table border="1">


        <colgroup>
           <col />
           <col />
           <col />
        </colgroup>

        <thead>
           <tr>
             <th scope="col">ESTACIÓN</th>
			 <th scope="col">A 2 DÍAS</th>
			 <th scope="col">A 3 DÍAS</th>	
			 <th scope="col">A 4 DÍAS</th>
			 <th scope="col">A 5 DÍAS</th>
			 <th scope="col">A 6 DÍAS</th>		
			 <th scope="col">A 7 DÍAS</th>			 
             <th scope="col">OTROS</th>
           </tr>
        </thead>


        <tbody>
           <tr>
             <th scope="row">Moncloa</th>
             <td>Muuuuchas 2</td>
             <td>Muuuuchas 3</td>
             <td>Muuuuchas 4</td>
             <td>Muuuuchas 5</td>
             <td>Muuuuchas 6</td>
			 <td>Muuuuchas 7</td>
             <td>Sol</td>
           </tr>
        </tbody> 
        <tbody>
           <tr>
             <th scope="row">Arganda del rey</th>
             <td>Pocas 2</td>
			 <td>Pocas 3</td>
			 <td>Pocas 4</td>
			 <td>Pocas 5</td>
			 <td>Pocas 6</td>
			 <td>Pocas 7</td>
             <td>Lluvia</td>
           </tr>
        </tbody>
 </table>

% include('footer.tpl')