% include('header_hoy.tpl', title='Niveles del día')
    <h1>{{name}}</h1>
		<img src="data:image/png;base64, {{plot_url}}">
		<p>Temperatura máxima:{{max}}ºC</p>
		<p>temperatura mínima:{{min}}ºC</p>
		<a href="../hoy">Volver</a>
% include('footer.tpl')