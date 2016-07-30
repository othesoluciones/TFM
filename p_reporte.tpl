% include('header_reporte.tpl', title='¡Repórtanos!')
	<h1>Repórtanos alertas</h1>

<table border="1">
	<form action="/reporta" method="post">


        <colgroup>
           <col />
           <col />
        </colgroup>


        <tbody>
           <tr>
             <th scope="row">Captador</th>
             <td><input name="captador" type="text" /></td>
           </tr>
        </tbody> 
        <tbody>
           <tr>
             <th scope="row">Nivel</th>
             <td><input name="nivel" type="text" /></td>
           </tr>
        </tbody>
		        <tbody>
           <tr>
             <th scope="row"></th>
             <td><input value="Enviar alerta" type="submit" /></td>
           </tr>
        </tbody>
	</form>			
 </table>
% include('footer.tpl')