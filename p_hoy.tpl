% include('header_hoy.tpl', title='Niveles del día', ndd=noticias_del_dia)
	<h1>Municipios de Madrid</h1>
	<div id="columns">
	<ul>
	% for m in muni:
		<li><a href="/{{m.attrib["value"][-5:]}}/{{m.text}}">{{m.text}}</a></li>
	%end
	</ul>
</div>
% include('footer.tpl')
