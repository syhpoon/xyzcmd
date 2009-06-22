<map version="0.8.1">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1244495427966" ID="Freemind_Link_1162096031" MODIFIED="1244501325179" TEXT="XYZCommander">
<font NAME="Tahoma" SIZE="12"/>
<node CREATED="1244495489656" ID="_" MODIFIED="1244501325177" POSITION="right" TEXT="UI">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244495492427" ID="Freemind_Link_513771550" MODIFIED="1244501325176" POSITION="left" TEXT="VFS">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244495503893" ID="Freemind_Link_1083954312" MODIFIED="1244501325175" POSITION="right" TEXT="Keys">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244495506843" ID="Freemind_Link_1669503816" MODIFIED="1244501325174" POSITION="left" TEXT="Plugins">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244495510007" ID="Freemind_Link_522268654" MODIFIED="1244501325173" POSITION="right" TEXT="Skins">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244495526482" ID="Freemind_Link_1653593100" MODIFIED="1244501325171" POSITION="left" TEXT="Parsers">
<edge COLOR="#0000cc"/>
<font NAME="Tahoma" SIZE="12"/>
<node CREATED="1244495535504" ID="Freemind_Link_1432536488" MODIFIED="1244501325171" TEXT="Block">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244495538897" ID="Freemind_Link_1256030206" MODIFIED="1244501325170" TEXT="Flat">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244495541619" ID="Freemind_Link_672743503" MODIFIED="1244501325168" TEXT="Multi">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244495544485" ID="Freemind_Link_1436796589" MODIFIED="1244501325167" TEXT="Regexp">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244500228761" ID="Freemind_Link_1274127063" MODIFIED="1244501325166" TEXT="LR">
<font NAME="Tahoma" SIZE="12"/>
<node CREATED="1244500237630" ID="Freemind_Link_863082863" MODIFIED="1244501325164" TEXT="FS-Rules">
<font NAME="Tahoma" SIZE="12"/>
</node>
</node>
<node CREATED="1244500242900" ID="Freemind_Link_1799785524" MODIFIED="1244501325162" TEXT="XYZScript">
<edge COLOR="#000066"/>
<cloud/>
<font NAME="Tahoma" SIZE="12"/>
<node CREATED="1244501362238" ID="Freemind_Link_1837826538" MODIFIED="1244501539906" TEXT="Purposes">
<node CREATED="1244500368153" ID="Freemind_Link_588763910" MODIFIED="1244501325161" STYLE="bubble" TEXT="Set variables">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244500357961" ID="Freemind_Link_377742210" MODIFIED="1244663219087" STYLE="bubble" TEXT="Set hooks">
<font NAME="Tahoma" SIZE="12"/>
<icon BUILTIN="help"/>
</node>
<node CREATED="1244500374558" ID="Freemind_Link_1724178337" MODIFIED="1244501325158" STYLE="bubble" TEXT="Set actions">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244500335413" ID="Freemind_Link_1404010742" MODIFIED="1244501325155" STYLE="bubble" TEXT="Define prefix keys">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244500346152" ID="Freemind_Link_1348615388" MODIFIED="1244501325154" STYLE="bubble" TEXT="Load plugins">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244500299809" ID="Freemind_Link_294604026" MODIFIED="1244501325151" STYLE="bubble" TEXT="Bind methods to shortcuts">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244500314560" ID="Freemind_Link_1710706342" MODIFIED="1244575214830" STYLE="bubble" TEXT="Call procedures">
<font NAME="Tahoma" SIZE="12"/>
</node>
<node CREATED="1244571892922" ID="Freemind_Link_255526285" MODIFIED="1244571899817" TEXT="Plugins configuration"/>
</node>
<node CREATED="1245357853679" ID="Freemind_Link_537964125" MODIFIED="1245357857793" TEXT="DSL">
<node CREATED="1245361398689" ID="Freemind_Link_855729037" MODIFIED="1245361403285" TEXT="interface">
<node CREATED="1245359440779" ID="Freemind_Link_1142229797" MODIFIED="1245368124565" TEXT="kbd(*keys)">
<node CREATED="1245360061472" ID="Freemind_Link_672485290" MODIFIED="1245360075054" TEXT="Create shortcut as a key sequence">
<node CREATED="1244662573839" ID="Freemind_Link_310059790" MODIFIED="1245585475712" TEXT="kbd(&quot;UP&quot;)&#xa;kbd(&quot;META-s&quot;, &quot;x&quot;)&#xa;kbd(&quot;CTRL-z&quot;)&#xa;kbd(&quot;F5&quot;)">
<icon BUILTIN="xmag"/>
</node>
</node>
</node>
<node CREATED="1245357873731" ID="Freemind_Link_1403521052" MODIFIED="1245456321892" TEXT="let(varname, value, section=&quot;local&quot;)">
<icon BUILTIN="button_ok"/>
<node CREATED="1245357962726" ID="Freemind_Link_275929665" MODIFIED="1245459340607" TEXT="Set variable.&#xa;Variable will be available in xyz.conf[section][varname]&#xa;If section is not provided - &quot;local&quot; will be used">
<node COLOR="#000000" CREATED="1244500518886" ID="Freemind_Link_70663728" MODIFIED="1245459281297" TEXT="let(&quot;myvar&quot;, &quot;some value&quot;) # xyz.conf[&quot;local&quot;][&quot;myvar&quot;] == &quot;some value&quot;&#xa;***&#xa;let(&quot;skin&quot;, &quot;blue&quot;, section=&quot;xyz&quot;)">
<font NAME="Tahoma" SIZE="12"/>
<icon BUILTIN="xmag"/>
</node>
</node>
</node>
<node CREATED="1245583541470" ID="Freemind_Link_502370608" MODIFIED="1245586759557" TEXT="unlet(var, sec=&quot;local&quot;)">
<icon BUILTIN="button_ok"/>
<node CREATED="1245583554322" ID="Freemind_Link_1904306065" MODIFIED="1245583559521" TEXT="Unset variable"/>
</node>
<node CREATED="1245358523711" ID="Freemind_Link_1001198349" MODIFIED="1245701446418" TEXT="action(rule, function)">
<icon BUILTIN="button_ok"/>
<node CREATED="1245358566594" ID="Freemind_Link_241216621" MODIFIED="1245358580145" TEXT="Set action based on rule to some function">
<node CREATED="1244663231419" ID="Freemind_Link_1449275902" MODIFIED="1245459373257" TEXT="action(r&quot;type{dir} or (link_type{dir} and link_exists{?})&quot;, lambda: call(&quot;:sys:panel:chdir&quot;, &quot;%O&quot;))">
<icon BUILTIN="xmag"/>
</node>
</node>
</node>
<node CREATED="1245358854608" ID="Freemind_Link_171194029" MODIFIED="1245358878285" TEXT="set_prefix(shortcut)">
<node CREATED="1245358880735" ID="Freemind_Link_1028978107" MODIFIED="1245358913602" TEXT="Set new prefix key">
<node CREATED="1244663685258" ID="Freemind_Link_1955451308" MODIFIED="1245358996993" TEXT="XYZ.set_prefix(XYZ.Shortcut(&quot;CTRL x&quot;))">
<icon BUILTIN="xmag"/>
</node>
</node>
</node>
<node CREATED="1245359317854" ID="Freemind_Link_1693687529" MODIFIED="1245456326217" TEXT="load(plugin)">
<icon BUILTIN="button_ok"/>
<node CREATED="1245359338973" ID="Freemind_Link_472092876" MODIFIED="1245359352695" TEXT="Load method[s] from plugin">
<node COLOR="#000000" CREATED="1244500656760" ID="Freemind_Link_1615115653" MODIFIED="1245359369649" TEXT="XYZ.load(&quot;sys:panel:*&quot;)">
<font NAME="Tahoma" SIZE="12"/>
<icon BUILTIN="xmag"/>
</node>
</node>
</node>
<node CREATED="1245359395521" ID="Freemind_Link_1708893538" MODIFIED="1245586759550" TEXT="bind(method, shortcut, context=&quot;@&quot;)">
<icon BUILTIN="button_ok"/>
<node CREATED="1245359455981" ID="Freemind_Link_1257852318" MODIFIED="1245359465408" TEXT="Bind specified method to shortcut">
<node COLOR="#000000" CREATED="1244500735764" ID="Freemind_Link_1761463976" MODIFIED="1245459397322" TEXT="bind(&quot;:sys:panel:entry_next&quot;, shortcut(&quot;DOWN&quot;), context=&quot;@&quot;)">
<font NAME="Tahoma" SIZE="12"/>
<icon BUILTIN="xmag"/>
</node>
</node>
</node>
<node CREATED="1245359544399" ID="Freemind_Link_118928829" MODIFIED="1245703180982" TEXT="call(method, *args)">
<icon BUILTIN="button_ok"/>
<node CREATED="1245359576515" ID="Freemind_Link_1569658164" MODIFIED="1245359587464" TEXT="Call plugin method on args">
<node CREATED="1245359588748" ID="Freemind_Link_1656389879" MODIFIED="1245359606267" TEXT="Substitutions">
<icon BUILTIN="help"/>
</node>
<node COLOR="#000000" CREATED="1244500844494" ID="Freemind_Link_1020330840" MODIFIED="1245359626362" TEXT="XYZ.call(&quot;:sys:panel:chdir&quot;, &quot;/&quot;)">
<font NAME="Tahoma" SIZE="12"/>
<icon BUILTIN="xmag"/>
</node>
</node>
</node>
<node CREATED="1245361152489" ID="Freemind_Link_890209027" MODIFIED="1245361159281" TEXT="hook()">
<icon BUILTIN="help"/>
</node>
<node CREATED="1245535477575" ID="Freemind_Link_1446723596" MODIFIED="1245703189796" TEXT="exec_file">
<icon BUILTIN="button_ok"/>
</node>
<node CREATED="1245615450750" ID="Freemind_Link_1513951905" MODIFIED="1245703195556" TEXT="macro(macro_name)">
<icon BUILTIN="button_ok"/>
<node CREATED="1245615481016" ID="Freemind_Link_816910859" MODIFIED="1245615487833" TEXT="Expand macro">
<node CREATED="1245615489117" ID="Freemind_Link_425587281" MODIFIED="1245615510487" TEXT="macro(&quot;CWD&quot;)"/>
</node>
</node>
</node>
<node CREATED="1245361428409" FOLDED="true" ID="Freemind_Link_940491710" MODIFIED="1245361436843" TEXT="Implementation">
<node CREATED="1245361507096" ID="Freemind_Link_981733442" MODIFIED="1245361539882" TEXT="XYZObject singleton"/>
<node CREATED="1245361641193" ID="Freemind_Link_1911204732" MODIFIED="1245361645041" TEXT="XYZShortcut"/>
</node>
</node>
</node>
</node>
</node>
</map>
