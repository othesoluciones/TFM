% include('header_notificaciones.tpl', title='Notificaciones')
	<h1>Recibe notificaciones</h1>

<table border="1">
	<form action="/notifica" method="post">

        <colgroup>
           <col />
           <col />
        </colgroup>


        <tbody>
           <tr>
             <th scope="row">Email</th>
             <td><input name="email" type="text" /></td>
           </tr>
        </tbody> 
        <tbody>
           <tr>
             <th scope="row">Captador</th>
             <td><input name="captador" type="text" /></td>
           </tr>
        </tbody>
        <tbody>
           <tr>
             <th scope="row">Periodicidad</th>
             <td><input name="periodicidad" type="text" /></td>
           </tr>
        </tbody>
		<tbody>
           <tr>
             <th scope="row"></th>
             <td><input value="Realizar suscripción" type="submit" /></td>
           </tr>
        </tbody>
	</form>	
 </table>
% include('footer.tpl')