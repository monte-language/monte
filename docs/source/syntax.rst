
Syntax Reference
================

.. raw:: html

    <style>
    svg.railroad-diagram {
        background-color: hsl(30,20%,95%);
    }
    svg.railroad-diagram path {
        stroke-width: 3;
        stroke: black;
        fill: rgba(0,0,0,0);
    }
    svg.railroad-diagram text {
        font: bold 14px monospace;
        text-anchor: middle;
    }
    svg.railroad-diagram text.label {
        text-anchor: start;
    }
    svg.railroad-diagram text.comment {
        font: italic 12px monospace;
    }
    svg.railroad-diagram g.non-terminal text {
        font-style: italic;
        font-weight: normal;
    }
    svg.railroad-diagram rect {
        stroke-width: 3;
        stroke: black;
        fill: hsl(120,100%,90%);
    }
    </style>

module
------

.. raw:: html

   <svg class="railroad-diagram" height="82" viewBox="0 0 501 82" width="501" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 41 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 51h0">
   </path><path d="M460 51h0">
   </path><g>
   <path d="M40 51h0">
   </path><path d="M380 51h0">
   </path><path d="M40 51a10 10 0 0 0 10 -10v-9a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M60 22h300">
   </path></g><path d="M360 22a10 10 0 0 1 10 10v9a10 10 0 0 0 10 10">
   </path><path d="M40 51h20">
   </path><g>
   <path d="M60 51h0">
   </path><path d="M360 51h0">
   </path><path d="M60 51h10">
   </path><g class="terminal">
   <path d="M70 51h0">
   </path><path d="M138 51h0">
   </path><rect height="22" rx="10" ry="10" width="68" x="70" y="40">
   </rect><text x="104" y="55">
   module</text></g><path d="M138 51h10">
   </path><path d="M148 51h10">
   </path><g class="non-terminal">
   <path d="M158 51h0">
   </path><path d="M234 51h0">
   </path><rect height="22" width="76" x="158" y="40">
   </rect><text x="196" y="55">
   imports</text></g><path d="M234 51h10">
   </path><g>
   <path d="M244 51h0">
   </path><path d="M360 51h0">
   </path><path d="M244 51a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M264 31h76">
   </path></g><path d="M340 31a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M244 51h20">
   </path><g class="non-terminal">
   <path d="M264 51h0">
   </path><path d="M340 51h0">
   </path><rect height="22" width="76" x="264" y="40">
   </rect><text x="302" y="55">
   exports</text></g><path d="M340 51h20">
   </path></g></g><path d="M360 51h20">
   </path></g><path d="M380 51h10">
   </path><g class="non-terminal">
   <path d="M390 51h0">
   </path><path d="M450 51h0">
   </path><rect height="22" width="60" x="390" y="40">
   </rect><text x="420" y="55">
   block</text></g><path d="M450 51h10">
   </path></g><path d="M 460 51 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

imports
-------

.. raw:: html

   <svg class="railroad-diagram" height="81" viewBox="0 0 217 81" width="217" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M176 41h0">
   </path><path d="M40 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M60 21h96">
   </path></g><path d="M156 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M40 41h20">
   </path><g>
   <path d="M60 41h0">
   </path><path d="M156 41h0">
   </path><path d="M60 41h10">
   </path><g class="non-terminal">
   <path d="M70 41h0">
   </path><path d="M146 41h0">
   </path><rect height="22" width="76" x="70" y="30">
   </rect><text x="108" y="45">
   pattern</text></g><path d="M146 41h10">
   </path><path d="M70 41a10 10 0 0 0 -10 10v0a10 10 0 0 0 10 10">
   </path><g>
   <path d="M70 61h76">
   </path></g><path d="M146 61a10 10 0 0 0 10 -10v0a10 10 0 0 0 -10 -10">
   </path></g><path d="M156 41h20">
   </path></g><path d="M 176 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

exports
-------

.. raw:: html

   <svg class="railroad-diagram" height="81" viewBox="0 0 377 81" width="377" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M336 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M118 41h0">
   </path><rect height="22" rx="10" ry="10" width="68" x="50" y="30">
   </rect><text x="84" y="45">
   export</text></g><path d="M118 41h10">
   </path><path d="M128 41h10">
   </path><g class="terminal">
   <path d="M138 41h0">
   </path><path d="M166 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="138" y="30">
   </rect><text x="152" y="45">
   (</text></g><path d="M166 41h10">
   </path><g>
   <path d="M176 41h0">
   </path><path d="M288 41h0">
   </path><path d="M176 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M196 21h72">
   </path></g><path d="M268 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M176 41h20">
   </path><g>
   <path d="M196 41h0">
   </path><path d="M268 41h0">
   </path><path d="M196 41h10">
   </path><g class="non-terminal">
   <path d="M206 41h0">
   </path><path d="M258 41h0">
   </path><rect height="22" width="52" x="206" y="30">
   </rect><text x="232" y="45">
   noun</text></g><path d="M258 41h10">
   </path><path d="M206 41a10 10 0 0 0 -10 10v0a10 10 0 0 0 10 10">
   </path><g>
   <path d="M206 61h52">
   </path></g><path d="M258 61a10 10 0 0 0 10 -10v0a10 10 0 0 0 -10 -10">
   </path></g><path d="M268 41h20">
   </path></g><path d="M288 41h10">
   </path><g class="terminal">
   <path d="M298 41h0">
   </path><path d="M326 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="298" y="30">
   </rect><text x="312" y="45">
   )</text></g><path d="M326 41h10">
   </path></g><path d="M 336 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

block
-----

.. raw:: html

   <svg class="railroad-diagram" height="162" viewBox="0 0 409 162" width="409" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M368 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M78 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="50" y="30">
   </rect><text x="64" y="45">
   {</text></g><path d="M78 41h10">
   </path><g>
   <path d="M88 41h0">
   </path><path d="M320 41h0">
   </path><path d="M88 41h20">
   </path><g>
   <path d="M108 41h0">
   </path><path d="M300 41h0">
   </path><path d="M108 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M128 21h152">
   </path></g><path d="M280 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M108 41h20">
   </path><g>
   <path d="M128 41h0">
   </path><path d="M280 41h0">
   </path><path d="M128 41h10">
   </path><g>
   <path d="M138 41h0">
   </path><path d="M270 41h0">
   </path><path d="M138 41h20">
   </path><g class="non-terminal">
   <path d="M158 41h0">
   </path><path d="M250 41h0">
   </path><rect height="22" width="92" x="158" y="30">
   </rect><text x="204" y="45">
   blockExpr</text></g><path d="M250 41h20">
   </path><path d="M138 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M158 71h20">
   </path><path d="M230 71h20">
   </path><rect height="22" width="52" x="178" y="60">
   </rect><text x="204" y="75">
   expr</text></g><path d="M250 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M270 41h10">
   </path><path d="M138 41a10 10 0 0 0 -10 10v40a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M138 101h52">
   </path><path d="M218 101h52">
   </path><rect height="22" rx="10" ry="10" width="28" x="190" y="90">
   </rect><text x="204" y="105">
   ;</text></g><path d="M270 101a10 10 0 0 0 10 -10v-40a10 10 0 0 0 -10 -10">
   </path></g><path d="M280 41h20">
   </path></g><path d="M300 41h20">
   </path><path d="M88 41a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M108 131h70">
   </path><path d="M230 131h70">
   </path><rect height="22" rx="10" ry="10" width="52" x="178" y="120">
   </rect><text x="204" y="135">
   pass</text></g><path d="M300 131a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path></g><path d="M320 41h10">
   </path><g class="terminal">
   <path d="M330 41h0">
   </path><path d="M358 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="330" y="30">
   </rect><text x="344" y="45">
   }</text></g><path d="M358 41h10">
   </path></g><path d="M 368 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

blockExpr
---------

.. raw:: html

   <svg class="railroad-diagram" height="422" viewBox="0 0 213 422" width="213" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M172 31h0">
   </path><path d="M40 31h20">
   </path><g class="non-terminal">
   <path d="M60 31h28">
   </path><path d="M124 31h28">
   </path><rect height="22" width="36" x="88" y="20">
   </rect><text x="106" y="35">
   if</text></g><path d="M152 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 61h12">
   </path><path d="M140 61h12">
   </path><rect height="22" width="68" x="72" y="50">
   </rect><text x="106" y="65">
   escape</text></g><path d="M152 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 91h24">
   </path><path d="M128 91h24">
   </path><rect height="22" width="44" x="84" y="80">
   </rect><text x="106" y="95">
   for</text></g><path d="M152 91a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 121h28">
   </path><path d="M124 121h28">
   </path><rect height="22" width="36" x="88" y="110">
   </rect><text x="106" y="125">
   fn</text></g><path d="M152 121a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v100a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 151h12">
   </path><path d="M140 151h12">
   </path><rect height="22" width="68" x="72" y="140">
   </rect><text x="106" y="155">
   switch</text></g><path d="M152 151a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v130a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 181h24">
   </path><path d="M128 181h24">
   </path><rect height="22" width="44" x="84" y="170">
   </rect><text x="106" y="185">
   try</text></g><path d="M152 181a10 10 0 0 0 10 -10v-130a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v160a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 211h16">
   </path><path d="M136 211h16">
   </path><rect height="22" width="60" x="76" y="200">
   </rect><text x="106" y="215">
   while</text></g><path d="M152 211a10 10 0 0 0 10 -10v-160a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v190a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 241h20">
   </path><path d="M132 241h20">
   </path><rect height="22" width="52" x="80" y="230">
   </rect><text x="106" y="245">
   when</text></g><path d="M152 241a10 10 0 0 0 10 -10v-190a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v220a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 271h20">
   </path><path d="M132 271h20">
   </path><rect height="22" width="52" x="80" y="260">
   </rect><text x="106" y="275">
   bind</text></g><path d="M152 271a10 10 0 0 0 10 -10v-220a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v250a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 301h12">
   </path><path d="M140 301h12">
   </path><rect height="22" width="68" x="72" y="290">
   </rect><text x="106" y="305">
   object</text></g><path d="M152 301a10 10 0 0 0 10 -10v-250a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v280a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 331h24">
   </path><path d="M128 331h24">
   </path><rect height="22" width="44" x="84" y="320">
   </rect><text x="106" y="335">
   def</text></g><path d="M152 331a10 10 0 0 0 10 -10v-280a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v310a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 361h0">
   </path><path d="M152 361h0">
   </path><rect height="22" width="92" x="60" y="350">
   </rect><text x="106" y="365">
   interface</text></g><path d="M152 361a10 10 0 0 0 10 -10v-310a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v340a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 391h20">
   </path><path d="M132 391h20">
   </path><rect height="22" width="52" x="80" y="380">
   </rect><text x="106" y="395">
   meta</text></g><path d="M152 391a10 10 0 0 0 10 -10v-340a10 10 0 0 1 10 -10">
   </path></g><path d="M 172 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

if
--

.. raw:: html

   <svg class="railroad-diagram" height="102" viewBox="0 0 700 102" width="700" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M659 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M86 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="50" y="30">
   </rect><text x="68" y="45">
   if</text></g><path d="M86 41h10">
   </path><path d="M96 41h10">
   </path><g class="terminal">
   <path d="M106 41h0">
   </path><path d="M134 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="106" y="30">
   </rect><text x="120" y="45">
   (</text></g><path d="M134 41h10">
   </path><path d="M144 41h10">
   </path><g class="non-terminal">
   <path d="M154 41h0">
   </path><path d="M206 41h0">
   </path><rect height="22" width="52" x="154" y="30">
   </rect><text x="180" y="45">
   expr</text></g><path d="M206 41h10">
   </path><path d="M216 41h10">
   </path><g class="terminal">
   <path d="M226 41h0">
   </path><path d="M254 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="226" y="30">
   </rect><text x="240" y="45">
   )</text></g><path d="M254 41h10">
   </path><path d="M264 41h10">
   </path><g class="non-terminal">
   <path d="M274 41h0">
   </path><path d="M334 41h0">
   </path><rect height="22" width="60" x="274" y="30">
   </rect><text x="304" y="45">
   block</text></g><path d="M334 41h10">
   </path><g>
   <path d="M344 41h0">
   </path><path d="M659 41h0">
   </path><path d="M344 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M364 21h275">
   </path></g><path d="M639 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M344 41h20">
   </path><g>
   <path d="M364 41h0">
   </path><path d="M639 41h0">
   </path><path d="M364 41h10">
   </path><g class="terminal">
   <path d="M374 41h0">
   </path><path d="M426 41h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="374" y="30">
   </rect><text x="400" y="45">
   else</text></g><path d="M426 41h10">
   </path><g>
   <path d="M436 41h0">
   </path><path d="M639 41h0">
   </path><path d="M436 41h20">
   </path><g>
   <path d="M456 41h0">
   </path><path d="M619 41h0">
   </path><path d="M456 41h10">
   </path><g class="terminal">
   <path d="M466 41h0">
   </path><path d="M502 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="466" y="30">
   </rect><text x="484" y="45">
   if</text></g><path d="M502 41h10">
   </path><path d="M512 41h10">
   </path><g>
   <path d="M522 41h0">
   </path><path d="M609 41h0">
   </path><text class="comment" x="565" y="46">
   blockExpr@@</text></g><path d="M609 41h10">
   </path></g><path d="M619 41h20">
   </path><path d="M436 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M456 71h51">
   </path><path d="M567 71h51">
   </path><rect height="22" width="60" x="507" y="60">
   </rect><text x="537" y="75">
   block</text></g><path d="M619 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g></g><path d="M639 41h20">
   </path></g></g><path d="M 659 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

escape
------

.. raw:: html

   <svg class="railroad-diagram" height="62" viewBox="0 0 385 62" width="385" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M344 31h0">
   </path><path d="M40 31h10">
   </path><g class="terminal">
   <path d="M50 31h0">
   </path><path d="M118 31h0">
   </path><rect height="22" rx="10" ry="10" width="68" x="50" y="20">
   </rect><text x="84" y="35">
   escape</text></g><path d="M118 31h10">
   </path><path d="M128 31h10">
   </path><g class="non-terminal">
   <path d="M138 31h0">
   </path><path d="M214 31h0">
   </path><rect height="22" width="76" x="138" y="20">
   </rect><text x="176" y="35">
   pattern</text></g><path d="M214 31h10">
   </path><path d="M224 31h10">
   </path><g class="non-terminal">
   <path d="M234 31h0">
   </path><path d="M334 31h0">
   </path><rect height="22" width="100" x="234" y="20">
   </rect><text x="284" y="35">
   blockCatch</text></g><path d="M334 31h10">
   </path></g><path d="M 344 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

blockCatch
----------

.. raw:: html

   <svg class="railroad-diagram" height="72" viewBox="0 0 457 72" width="457" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M416 41h0">
   </path><path d="M40 41h10">
   </path><g class="non-terminal">
   <path d="M50 41h0">
   </path><path d="M110 41h0">
   </path><rect height="22" width="60" x="50" y="30">
   </rect><text x="80" y="45">
   block</text></g><path d="M110 41h10">
   </path><g>
   <path d="M120 41h0">
   </path><path d="M416 41h0">
   </path><path d="M120 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M140 21h256">
   </path></g><path d="M396 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M120 41h20">
   </path><g>
   <path d="M140 41h0">
   </path><path d="M396 41h0">
   </path><path d="M140 41h10">
   </path><g class="terminal">
   <path d="M150 41h0">
   </path><path d="M210 41h0">
   </path><rect height="22" rx="10" ry="10" width="60" x="150" y="30">
   </rect><text x="180" y="45">
   catch</text></g><path d="M210 41h10">
   </path><path d="M220 41h10">
   </path><g class="non-terminal">
   <path d="M230 41h0">
   </path><path d="M306 41h0">
   </path><rect height="22" width="76" x="230" y="30">
   </rect><text x="268" y="45">
   pattern</text></g><path d="M306 41h10">
   </path><path d="M316 41h10">
   </path><g class="non-terminal">
   <path d="M326 41h0">
   </path><path d="M386 41h0">
   </path><rect height="22" width="60" x="326" y="30">
   </rect><text x="356" y="45">
   block</text></g><path d="M386 41h10">
   </path></g><path d="M396 41h20">
   </path></g></g><path d="M 416 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

for
---

.. raw:: html

   <svg class="railroad-diagram" height="72" viewBox="0 0 681 72" width="681" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M640 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M94 41h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="50" y="30">
   </rect><text x="72" y="45">
   for</text></g><path d="M94 41h10">
   </path><path d="M104 41h10">
   </path><g class="non-terminal">
   <path d="M114 41h0">
   </path><path d="M190 41h0">
   </path><rect height="22" width="76" x="114" y="30">
   </rect><text x="152" y="45">
   pattern</text></g><path d="M190 41h10">
   </path><g>
   <path d="M200 41h0">
   </path><path d="M392 41h0">
   </path><path d="M200 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M220 21h152">
   </path></g><path d="M372 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M200 41h20">
   </path><g>
   <path d="M220 41h0">
   </path><path d="M372 41h0">
   </path><path d="M220 41h10">
   </path><g class="terminal">
   <path d="M230 41h0">
   </path><path d="M266 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="230" y="30">
   </rect><text x="248" y="45">
   =></text></g><path d="M266 41h10">
   </path><path d="M276 41h10">
   </path><g class="non-terminal">
   <path d="M286 41h0">
   </path><path d="M362 41h0">
   </path><rect height="22" width="76" x="286" y="30">
   </rect><text x="324" y="45">
   pattern</text></g><path d="M362 41h10">
   </path></g><path d="M372 41h20">
   </path></g><path d="M392 41h10">
   </path><g class="terminal">
   <path d="M402 41h0">
   </path><path d="M438 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="402" y="30">
   </rect><text x="420" y="45">
   in</text></g><path d="M438 41h10">
   </path><path d="M448 41h10">
   </path><g class="non-terminal">
   <path d="M458 41h0">
   </path><path d="M510 41h0">
   </path><rect height="22" width="52" x="458" y="30">
   </rect><text x="484" y="45">
   comp</text></g><path d="M510 41h10">
   </path><path d="M520 41h10">
   </path><g class="non-terminal">
   <path d="M530 41h0">
   </path><path d="M630 41h0">
   </path><rect height="22" width="100" x="530" y="30">
   </rect><text x="580" y="45">
   blockCatch</text></g><path d="M630 41h10">
   </path></g><path d="M 640 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

fn
--

.. raw:: html

   <svg class="railroad-diagram" height="102" viewBox="0 0 353 102" width="353" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M312 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M86 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="50" y="30">
   </rect><text x="68" y="45">
   fn</text></g><path d="M86 41h10">
   </path><g>
   <path d="M96 41h0">
   </path><path d="M232 41h0">
   </path><path d="M96 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M116 21h96">
   </path></g><path d="M212 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M96 41h20">
   </path><g>
   <path d="M116 41h0">
   </path><path d="M212 41h0">
   </path><path d="M116 41h10">
   </path><g class="non-terminal">
   <path d="M126 41h0">
   </path><path d="M202 41h0">
   </path><rect height="22" width="76" x="126" y="30">
   </rect><text x="164" y="45">
   pattern</text></g><path d="M202 41h10">
   </path><path d="M126 41a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M126 71h24">
   </path><path d="M178 71h24">
   </path><rect height="22" rx="10" ry="10" width="28" x="150" y="60">
   </rect><text x="164" y="75">
   ,</text></g><path d="M202 71a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M212 41h20">
   </path></g><path d="M232 41h10">
   </path><g class="non-terminal">
   <path d="M242 41h0">
   </path><path d="M302 41h0">
   </path><rect height="22" width="60" x="242" y="30">
   </rect><text x="272" y="45">
   block</text></g><path d="M302 41h10">
   </path></g><path d="M 312 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

switch
------

.. raw:: html

   <svg class="railroad-diagram" height="71" viewBox="0 0 729 71" width="729" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M688 31h0">
   </path><path d="M40 31h10">
   </path><g class="terminal">
   <path d="M50 31h0">
   </path><path d="M118 31h0">
   </path><rect height="22" rx="10" ry="10" width="68" x="50" y="20">
   </rect><text x="84" y="35">
   switch</text></g><path d="M118 31h10">
   </path><path d="M128 31h10">
   </path><g class="terminal">
   <path d="M138 31h0">
   </path><path d="M166 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="138" y="20">
   </rect><text x="152" y="35">
   (</text></g><path d="M166 31h10">
   </path><path d="M176 31h10">
   </path><g class="non-terminal">
   <path d="M186 31h0">
   </path><path d="M238 31h0">
   </path><rect height="22" width="52" x="186" y="20">
   </rect><text x="212" y="35">
   expr</text></g><path d="M238 31h10">
   </path><path d="M248 31h10">
   </path><g class="terminal">
   <path d="M258 31h0">
   </path><path d="M286 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="258" y="20">
   </rect><text x="272" y="35">
   )</text></g><path d="M286 31h10">
   </path><path d="M296 31h10">
   </path><g class="terminal">
   <path d="M306 31h0">
   </path><path d="M334 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="306" y="20">
   </rect><text x="320" y="35">
   {</text></g><path d="M334 31h10">
   </path><path d="M344 31h10">
   </path><g>
   <path d="M354 31h0">
   </path><path d="M630 31h0">
   </path><path d="M354 31h10">
   </path><g>
   <path d="M364 31h0">
   </path><path d="M620 31h0">
   </path><path d="M364 31h10">
   </path><g class="terminal">
   <path d="M374 31h0">
   </path><path d="M434 31h0">
   </path><rect height="22" rx="10" ry="10" width="60" x="374" y="20">
   </rect><text x="404" y="35">
   match</text></g><path d="M434 31h10">
   </path><path d="M444 31h10">
   </path><g class="non-terminal">
   <path d="M454 31h0">
   </path><path d="M530 31h0">
   </path><rect height="22" width="76" x="454" y="20">
   </rect><text x="492" y="35">
   pattern</text></g><path d="M530 31h10">
   </path><path d="M540 31h10">
   </path><g class="non-terminal">
   <path d="M550 31h0">
   </path><path d="M610 31h0">
   </path><rect height="22" width="60" x="550" y="20">
   </rect><text x="580" y="35">
   block</text></g><path d="M610 31h10">
   </path></g><path d="M620 31h10">
   </path><path d="M364 31a10 10 0 0 0 -10 10v0a10 10 0 0 0 10 10">
   </path><g>
   <path d="M364 51h256">
   </path></g><path d="M620 51a10 10 0 0 0 10 -10v0a10 10 0 0 0 -10 -10">
   </path></g><path d="M630 31h10">
   </path><path d="M640 31h10">
   </path><g class="terminal">
   <path d="M650 31h0">
   </path><path d="M678 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="650" y="20">
   </rect><text x="664" y="35">
   }</text></g><path d="M678 31h10">
   </path></g><path d="M 688 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

try
---

.. raw:: html

   <svg class="railroad-diagram" height="62" viewBox="0 0 329 62" width="329" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M288 31h0">
   </path><path d="M40 31h10">
   </path><g class="terminal">
   <path d="M50 31h0">
   </path><path d="M94 31h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="50" y="20">
   </rect><text x="72" y="35">
   try</text></g><path d="M94 31h10">
   </path><path d="M104 31h10">
   </path><g class="non-terminal">
   <path d="M114 31h0">
   </path><path d="M174 31h0">
   </path><rect height="22" width="60" x="114" y="20">
   </rect><text x="144" y="35">
   block</text></g><path d="M174 31h10">
   </path><path d="M184 31h10">
   </path><g class="non-terminal">
   <path d="M194 31h0">
   </path><path d="M278 31h0">
   </path><rect height="22" width="84" x="194" y="20">
   </rect><text x="236" y="35">
   catchers</text></g><path d="M278 31h10">
   </path></g><path d="M 288 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

catchers
--------

.. raw:: html

   <svg class="railroad-diagram" height="81" viewBox="0 0 613 81" width="613" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M572 41h0">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M356 41h0">
   </path><path d="M40 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M60 21h276">
   </path></g><path d="M336 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M40 41h20">
   </path><g>
   <path d="M60 41h0">
   </path><path d="M336 41h0">
   </path><path d="M60 41h10">
   </path><g>
   <path d="M70 41h0">
   </path><path d="M326 41h0">
   </path><path d="M70 41h10">
   </path><g class="terminal">
   <path d="M80 41h0">
   </path><path d="M140 41h0">
   </path><rect height="22" rx="10" ry="10" width="60" x="80" y="30">
   </rect><text x="110" y="45">
   catch</text></g><path d="M140 41h10">
   </path><path d="M150 41h10">
   </path><g class="non-terminal">
   <path d="M160 41h0">
   </path><path d="M236 41h0">
   </path><rect height="22" width="76" x="160" y="30">
   </rect><text x="198" y="45">
   pattern</text></g><path d="M236 41h10">
   </path><path d="M246 41h10">
   </path><g class="non-terminal">
   <path d="M256 41h0">
   </path><path d="M316 41h0">
   </path><rect height="22" width="60" x="256" y="30">
   </rect><text x="286" y="45">
   block</text></g><path d="M316 41h10">
   </path></g><path d="M326 41h10">
   </path><path d="M70 41a10 10 0 0 0 -10 10v0a10 10 0 0 0 10 10">
   </path><g>
   <path d="M70 61h256">
   </path></g><path d="M326 61a10 10 0 0 0 10 -10v0a10 10 0 0 0 -10 -10">
   </path></g><path d="M336 41h20">
   </path></g><g>
   <path d="M356 41h0">
   </path><path d="M572 41h0">
   </path><path d="M356 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M376 21h176">
   </path></g><path d="M552 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M356 41h20">
   </path><g>
   <path d="M376 41h0">
   </path><path d="M552 41h0">
   </path><path d="M376 41h10">
   </path><g class="terminal">
   <path d="M386 41h0">
   </path><path d="M462 41h0">
   </path><rect height="22" rx="10" ry="10" width="76" x="386" y="30">
   </rect><text x="424" y="45">
   finally</text></g><path d="M462 41h10">
   </path><path d="M472 41h10">
   </path><g class="non-terminal">
   <path d="M482 41h0">
   </path><path d="M542 41h0">
   </path><rect height="22" width="60" x="482" y="30">
   </rect><text x="512" y="45">
   block</text></g><path d="M542 41h10">
   </path></g><path d="M552 41h20">
   </path></g></g><path d="M 572 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

while
-----

.. raw:: html

   <svg class="railroad-diagram" height="62" viewBox="0 0 449 62" width="449" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M408 31h0">
   </path><path d="M40 31h10">
   </path><g class="terminal">
   <path d="M50 31h0">
   </path><path d="M110 31h0">
   </path><rect height="22" rx="10" ry="10" width="60" x="50" y="20">
   </rect><text x="80" y="35">
   while</text></g><path d="M110 31h10">
   </path><path d="M120 31h10">
   </path><g class="terminal">
   <path d="M130 31h0">
   </path><path d="M158 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="130" y="20">
   </rect><text x="144" y="35">
   (</text></g><path d="M158 31h10">
   </path><path d="M168 31h10">
   </path><g class="non-terminal">
   <path d="M178 31h0">
   </path><path d="M230 31h0">
   </path><rect height="22" width="52" x="178" y="20">
   </rect><text x="204" y="35">
   expr</text></g><path d="M230 31h10">
   </path><path d="M240 31h10">
   </path><g class="terminal">
   <path d="M250 31h0">
   </path><path d="M278 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="250" y="20">
   </rect><text x="264" y="35">
   )</text></g><path d="M278 31h10">
   </path><path d="M288 31h10">
   </path><g class="non-terminal">
   <path d="M298 31h0">
   </path><path d="M398 31h0">
   </path><rect height="22" width="100" x="298" y="20">
   </rect><text x="348" y="35">
   blockCatch</text></g><path d="M398 31h10">
   </path></g><path d="M 408 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

when
----

.. raw:: html

   <svg class="railroad-diagram" height="92" viewBox="0 0 581 92" width="581" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M540 31h0">
   </path><path d="M40 31h10">
   </path><g class="terminal">
   <path d="M50 31h0">
   </path><path d="M102 31h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="50" y="20">
   </rect><text x="76" y="35">
   when</text></g><path d="M102 31h10">
   </path><path d="M112 31h10">
   </path><g class="terminal">
   <path d="M122 31h0">
   </path><path d="M150 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="122" y="20">
   </rect><text x="136" y="35">
   (</text></g><path d="M150 31h10">
   </path><path d="M160 31h10">
   </path><g>
   <path d="M170 31h0">
   </path><path d="M242 31h0">
   </path><path d="M170 31h10">
   </path><g class="non-terminal">
   <path d="M180 31h0">
   </path><path d="M232 31h0">
   </path><rect height="22" width="52" x="180" y="20">
   </rect><text x="206" y="35">
   expr</text></g><path d="M232 31h10">
   </path><path d="M180 31a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M180 61h12">
   </path><path d="M220 61h12">
   </path><rect height="22" rx="10" ry="10" width="28" x="192" y="50">
   </rect><text x="206" y="65">
   ,</text></g><path d="M232 61a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M242 31h10">
   </path><path d="M252 31h10">
   </path><g class="terminal">
   <path d="M262 31h0">
   </path><path d="M290 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="262" y="20">
   </rect><text x="276" y="35">
   )</text></g><path d="M290 31h10">
   </path><path d="M300 31h10">
   </path><g class="terminal">
   <path d="M310 31h0">
   </path><path d="M346 31h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="310" y="20">
   </rect><text x="328" y="35">
   -></text></g><path d="M346 31h10">
   </path><path d="M356 31h10">
   </path><g class="non-terminal">
   <path d="M366 31h0">
   </path><path d="M426 31h0">
   </path><rect height="22" width="60" x="366" y="20">
   </rect><text x="396" y="35">
   block</text></g><path d="M426 31h10">
   </path><path d="M436 31h10">
   </path><g class="non-terminal">
   <path d="M446 31h0">
   </path><path d="M530 31h0">
   </path><rect height="22" width="84" x="446" y="20">
   </rect><text x="488" y="35">
   catchers</text></g><path d="M530 31h10">
   </path></g><path d="M 540 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

bind
----

.. raw:: html

   <svg class="railroad-diagram" height="72" viewBox="0 0 439 72" width="439" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M398 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M102 41h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="50" y="30">
   </rect><text x="76" y="45">
   bind</text></g><path d="M102 41h10">
   </path><path d="M112 41h10">
   </path><g class="non-terminal">
   <path d="M122 41h0">
   </path><path d="M174 41h0">
   </path><rect height="22" width="52" x="122" y="30">
   </rect><text x="148" y="45">
   noun</text></g><path d="M174 41h10">
   </path><g>
   <path d="M184 41h0">
   </path><path d="M284 41h0">
   </path><path d="M184 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M204 21h60">
   </path></g><path d="M264 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M184 41h20">
   </path><g class="non-terminal">
   <path d="M204 41h0">
   </path><path d="M264 41h0">
   </path><rect height="22" width="60" x="204" y="30">
   </rect><text x="234" y="45">
   guard</text></g><path d="M264 41h20">
   </path></g><path d="M284 41h10">
   </path><g>
   <path d="M294 41h0">
   </path><path d="M388 41h0">
   </path><text class="comment" x="341" y="46">
   objectExpr@@</text></g><path d="M388 41h10">
   </path></g><path d="M 398 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

object
------

.. raw:: html

   <svg class="railroad-diagram" height="132" viewBox="0 0 567 132" width="567" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M526 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M118 41h0">
   </path><rect height="22" rx="10" ry="10" width="68" x="50" y="30">
   </rect><text x="84" y="45">
   object</text></g><path d="M118 41h10">
   </path><g>
   <path d="M128 41h0">
   </path><path d="M312 41h0">
   </path><path d="M128 41h20">
   </path><g>
   <path d="M148 41h0">
   </path><path d="M292 41h0">
   </path><path d="M148 41h10">
   </path><g class="terminal">
   <path d="M158 41h0">
   </path><path d="M210 41h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="158" y="30">
   </rect><text x="184" y="45">
   bind</text></g><path d="M210 41h10">
   </path><path d="M220 41h10">
   </path><g class="non-terminal">
   <path d="M230 41h0">
   </path><path d="M282 41h0">
   </path><rect height="22" width="52" x="230" y="30">
   </rect><text x="256" y="45">
   noun</text></g><path d="M282 41h10">
   </path></g><path d="M292 41h20">
   </path><path d="M128 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M148 71h58">
   </path><path d="M234 71h58">
   </path><rect height="22" rx="10" ry="10" width="28" x="206" y="60">
   </rect><text x="220" y="75">
   _</text></g><path d="M292 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M128 41a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M148 101h46">
   </path><path d="M246 101h46">
   </path><rect height="22" width="52" x="194" y="90">
   </rect><text x="220" y="105">
   noun</text></g><path d="M292 101a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M312 41h0">
   </path><path d="M412 41h0">
   </path><path d="M312 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M332 21h60">
   </path></g><path d="M392 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M312 41h20">
   </path><g class="non-terminal">
   <path d="M332 41h0">
   </path><path d="M392 41h0">
   </path><rect height="22" width="60" x="332" y="30">
   </rect><text x="362" y="45">
   guard</text></g><path d="M392 41h20">
   </path></g><path d="M412 41h10">
   </path><g>
   <path d="M422 41h0">
   </path><path d="M516 41h0">
   </path><text class="comment" x="469" y="46">
   objectExpr@@</text></g><path d="M516 41h10">
   </path></g><path d="M 526 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

objectExpr
----------

.. raw:: html

   <svg class="railroad-diagram" height="102" viewBox="0 0 673 102" width="673" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M632 41h0">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M256 41h0">
   </path><path d="M40 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M60 21h176">
   </path></g><path d="M236 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M40 41h20">
   </path><g>
   <path d="M60 41h0">
   </path><path d="M236 41h0">
   </path><path d="M60 41h10">
   </path><g class="terminal">
   <path d="M70 41h0">
   </path><path d="M146 41h0">
   </path><rect height="22" rx="10" ry="10" width="76" x="70" y="30">
   </rect><text x="108" y="45">
   extends</text></g><path d="M146 41h10">
   </path><path d="M156 41h10">
   </path><g class="non-terminal">
   <path d="M166 41h0">
   </path><path d="M226 41h0">
   </path><rect height="22" width="60" x="166" y="30">
   </rect><text x="196" y="45">
   order</text></g><path d="M226 41h10">
   </path></g><path d="M236 41h20">
   </path></g><path d="M256 41h10">
   </path><g class="non-terminal">
   <path d="M266 41h0">
   </path><path d="M350 41h0">
   </path><rect height="22" width="84" x="266" y="30">
   </rect><text x="308" y="45">
   auditors</text></g><path d="M350 41h10">
   </path><path d="M360 41h10">
   </path><g class="terminal">
   <path d="M370 41h0">
   </path><path d="M398 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="370" y="30">
   </rect><text x="384" y="45">
   {</text></g><path d="M398 41h10">
   </path><g>
   <path d="M408 41h0">
   </path><path d="M584 41h0">
   </path><path d="M408 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M428 21h136">
   </path></g><path d="M564 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M408 41h20">
   </path><g>
   <path d="M428 41h0">
   </path><path d="M564 41h0">
   </path><path d="M428 41h10">
   </path><g class="non-terminal">
   <path d="M438 41h0">
   </path><path d="M554 41h0">
   </path><rect height="22" width="116" x="438" y="30">
   </rect><text x="496" y="45">
   objectScript</text></g><path d="M554 41h10">
   </path><path d="M438 41a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M438 71h44">
   </path><path d="M510 71h44">
   </path><rect height="22" rx="10" ry="10" width="28" x="482" y="60">
   </rect><text x="496" y="75">
   ;</text></g><path d="M554 71a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M564 41h20">
   </path></g><path d="M584 41h10">
   </path><g class="terminal">
   <path d="M594 41h0">
   </path><path d="M622 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="594" y="30">
   </rect><text x="608" y="45">
   }</text></g><path d="M622 41h10">
   </path></g><path d="M 632 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

objectScript
------------

.. raw:: html

   <svg class="railroad-diagram" height="121" viewBox="0 0 541 121" width="541" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M500 41h0">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M132 41h0">
   </path><path d="M40 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M60 21h52">
   </path></g><path d="M112 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M40 41h20">
   </path><g class="non-terminal">
   <path d="M60 41h0">
   </path><path d="M112 41h0">
   </path><rect height="22" width="52" x="60" y="30">
   </rect><text x="86" y="45">
   doco</text></g><path d="M112 41h20">
   </path></g><g>
   <path d="M132 41h0">
   </path><path d="M300 41h0">
   </path><path d="M132 41h20">
   </path><g class="terminal">
   <path d="M152 41h38">
   </path><path d="M242 41h38">
   </path><rect height="22" rx="10" ry="10" width="52" x="190" y="30">
   </rect><text x="216" y="45">
   pass</text></g><path d="M280 41h20">
   </path><path d="M132 41a10 10 0 0 1 10 10v20a10 10 0 0 0 10 10">
   </path><g>
   <path d="M152 81h0">
   </path><path d="M280 81h0">
   </path><path d="M152 81a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M172 61h88">
   </path></g><path d="M260 61a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M152 81h20">
   </path><g>
   <path d="M172 81h0">
   </path><path d="M260 81h0">
   </path><path d="M172 81h10">
   </path><g class="terminal">
   <path d="M182 81h0">
   </path><path d="M250 81h0">
   </path><rect height="22" rx="10" ry="10" width="68" x="182" y="70">
   </rect><text x="216" y="85">
   @@meth</text></g><path d="M250 81h10">
   </path><path d="M182 81a10 10 0 0 0 -10 10v0a10 10 0 0 0 10 10">
   </path><g>
   <path d="M182 101h68">
   </path></g><path d="M250 101a10 10 0 0 0 10 -10v0a10 10 0 0 0 -10 -10">
   </path></g><path d="M260 81h20">
   </path></g><path d="M280 81a10 10 0 0 0 10 -10v-20a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M300 41h0">
   </path><path d="M500 41h0">
   </path><path d="M300 41h20">
   </path><g class="terminal">
   <path d="M320 41h54">
   </path><path d="M426 41h54">
   </path><rect height="22" rx="10" ry="10" width="52" x="374" y="30">
   </rect><text x="400" y="45">
   pass</text></g><path d="M480 41h20">
   </path><path d="M300 41a10 10 0 0 1 10 10v20a10 10 0 0 0 10 10">
   </path><g>
   <path d="M320 81h0">
   </path><path d="M480 81h0">
   </path><path d="M320 81a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M340 61h120">
   </path></g><path d="M460 61a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M320 81h20">
   </path><g>
   <path d="M340 81h0">
   </path><path d="M460 81h0">
   </path><path d="M340 81h10">
   </path><g class="terminal">
   <path d="M350 81h0">
   </path><path d="M450 81h0">
   </path><rect height="22" rx="10" ry="10" width="100" x="350" y="70">
   </rect><text x="400" y="85">
   @@matchers</text></g><path d="M450 81h10">
   </path><path d="M350 81a10 10 0 0 0 -10 10v0a10 10 0 0 0 10 10">
   </path><g>
   <path d="M350 101h100">
   </path></g><path d="M450 101a10 10 0 0 0 10 -10v0a10 10 0 0 0 -10 -10">
   </path></g><path d="M460 81h20">
   </path></g><path d="M480 81a10 10 0 0 0 10 -10v-20a10 10 0 0 1 10 -10">
   </path></g></g><path d="M 500 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

doco
----

.. raw:: html

   <svg class="railroad-diagram" height="62" viewBox="0 0 177 62" width="177" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><path d="M40 31h10">
   </path><g class="terminal">
   <path d="M50 31h0">
   </path><path d="M126 31h0">
   </path><rect height="22" rx="10" ry="10" width="76" x="50" y="20">
   </rect><text x="88" y="35">
   .String</text></g><path d="M126 31h10">
   </path><path d="M 136 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

def
---

.. raw:: html

   <svg class="railroad-diagram" height="132" viewBox="0 0 631 132" width="631" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M590 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M94 41h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="50" y="30">
   </rect><text x="72" y="45">
   def</text></g><path d="M94 41h10">
   </path><g>
   <path d="M104 41h0">
   </path><path d="M590 41h0">
   </path><path d="M104 41h20">
   </path><g>
   <path d="M124 41h0">
   </path><path d="M570 41h0">
   </path><g>
   <path d="M124 41h0">
   </path><path d="M408 41h0">
   </path><path d="M124 41h20">
   </path><g>
   <path d="M144 41h0">
   </path><path d="M388 41h0">
   </path><path d="M144 41h10">
   </path><g class="terminal">
   <path d="M154 41h0">
   </path><path d="M206 41h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="154" y="30">
   </rect><text x="180" y="45">
   bind</text></g><path d="M206 41h10">
   </path><path d="M216 41h10">
   </path><g class="non-terminal">
   <path d="M226 41h0">
   </path><path d="M278 41h0">
   </path><rect height="22" width="52" x="226" y="30">
   </rect><text x="252" y="45">
   noun</text></g><path d="M278 41h10">
   </path><g>
   <path d="M288 41h0">
   </path><path d="M388 41h0">
   </path><path d="M288 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M308 21h60">
   </path></g><path d="M368 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M288 41h20">
   </path><g class="non-terminal">
   <path d="M308 41h0">
   </path><path d="M368 41h0">
   </path><rect height="22" width="60" x="308" y="30">
   </rect><text x="338" y="45">
   guard</text></g><path d="M368 41h20">
   </path></g></g><path d="M388 41h20">
   </path><path d="M124 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M144 71h96">
   </path><path d="M292 71h96">
   </path><rect height="22" width="52" x="240" y="60">
   </rect><text x="266" y="75">
   noun</text></g><path d="M388 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M408 41h0">
   </path><path d="M570 41h0">
   </path><path d="M408 41h20">
   </path><g>
   <path d="M428 41h0">
   </path><path d="M550 41h0">
   </path><text class="comment" x="489" y="46">
   objectFunction@@</text></g><path d="M550 41h20">
   </path><path d="M408 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M428 71h27">
   </path><path d="M523 71h27">
   </path><rect height="22" width="68" x="455" y="60">
   </rect><text x="489" y="75">
   assign</text></g><path d="M550 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g></g><path d="M570 41h20">
   </path><path d="M104 41a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M124 101h189">
   </path><path d="M381 101h189">
   </path><rect height="22" width="68" x="313" y="90">
   </rect><text x="347" y="105">
   assign</text></g><path d="M570 101a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path></g></g><path d="M 590 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

interface
---------

.. raw:: html

   <svg class="railroad-diagram" height="102" viewBox="0 0 974 102" width="974" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M933 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M142 41h0">
   </path><rect height="22" rx="10" ry="10" width="92" x="50" y="30">
   </rect><text x="96" y="45">
   interface</text></g><path d="M142 41h10">
   </path><path d="M152 41h10">
   </path><g class="non-terminal">
   <path d="M162 41h0">
   </path><path d="M270 41h0">
   </path><rect height="22" width="108" x="162" y="30">
   </rect><text x="216" y="45">
   namePattern</text></g><path d="M270 41h10">
   </path><g>
   <path d="M280 41h0">
   </path><path d="M504 41h0">
   </path><path d="M280 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M300 21h184">
   </path></g><path d="M484 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M280 41h20">
   </path><g>
   <path d="M300 41h0">
   </path><path d="M484 41h0">
   </path><path d="M300 41h10">
   </path><g class="terminal">
   <path d="M310 41h0">
   </path><path d="M378 41h0">
   </path><rect height="22" rx="10" ry="10" width="68" x="310" y="30">
   </rect><text x="344" y="45">
   guards</text></g><path d="M378 41h10">
   </path><path d="M388 41h10">
   </path><g class="non-terminal">
   <path d="M398 41h0">
   </path><path d="M474 41h0">
   </path><rect height="22" width="76" x="398" y="30">
   </rect><text x="436" y="45">
   pattern</text></g><path d="M474 41h10">
   </path></g><path d="M484 41h20">
   </path></g><g>
   <path d="M504 41h0">
   </path><path d="M740 41h0">
   </path><path d="M504 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M524 21h196">
   </path></g><path d="M720 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M504 41h20">
   </path><g>
   <path d="M524 41h0">
   </path><path d="M720 41h0">
   </path><path d="M524 41h10">
   </path><g class="terminal">
   <path d="M534 41h0">
   </path><path d="M610 41h0">
   </path><rect height="22" rx="10" ry="10" width="76" x="534" y="30">
   </rect><text x="572" y="45">
   extends</text></g><path d="M610 41h10">
   </path><path d="M620 41h10">
   </path><g>
   <path d="M630 41h0">
   </path><path d="M710 41h0">
   </path><path d="M630 41h10">
   </path><g class="non-terminal">
   <path d="M640 41h0">
   </path><path d="M700 41h0">
   </path><rect height="22" width="60" x="640" y="30">
   </rect><text x="670" y="45">
   order</text></g><path d="M700 41h10">
   </path><path d="M640 41a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M640 71h16">
   </path><path d="M684 71h16">
   </path><rect height="22" rx="10" ry="10" width="28" x="656" y="60">
   </rect><text x="670" y="75">
   ,</text></g><path d="M700 71a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M710 41h10">
   </path></g><path d="M720 41h20">
   </path></g><path d="M740 41h10">
   </path><g>
   <path d="M750 41h0">
   </path><path d="M851 41h0">
   </path><text class="comment" x="800" y="46">
   implements_@@</text></g><path d="M851 41h10">
   </path><path d="M861 41h10">
   </path><g>
   <path d="M871 41h0">
   </path><path d="M923 41h0">
   </path><text class="comment" x="897" y="46">
   msgs@@</text></g><path d="M923 41h10">
   </path></g><path d="M 933 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

meta
----

.. raw:: html

   <svg class="railroad-diagram" height="92" viewBox="0 0 441 92" width="441" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M400 31h0">
   </path><path d="M40 31h10">
   </path><g class="terminal">
   <path d="M50 31h0">
   </path><path d="M102 31h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="50" y="20">
   </rect><text x="76" y="35">
   meta</text></g><path d="M102 31h10">
   </path><path d="M112 31h10">
   </path><g class="terminal">
   <path d="M122 31h0">
   </path><path d="M150 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="122" y="20">
   </rect><text x="136" y="35">
   .</text></g><path d="M150 31h10">
   </path><g>
   <path d="M160 31h0">
   </path><path d="M400 31h0">
   </path><path d="M160 31h20">
   </path><g>
   <path d="M180 31h4">
   </path><path d="M376 31h4">
   </path><path d="M184 31h10">
   </path><g class="terminal">
   <path d="M194 31h0">
   </path><path d="M270 31h0">
   </path><rect height="22" rx="10" ry="10" width="76" x="194" y="20">
   </rect><text x="232" y="35">
   context</text></g><path d="M270 31h10">
   </path><path d="M280 31h10">
   </path><g class="terminal">
   <path d="M290 31h0">
   </path><path d="M318 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="290" y="20">
   </rect><text x="304" y="35">
   (</text></g><path d="M318 31h10">
   </path><path d="M328 31h10">
   </path><g class="terminal">
   <path d="M338 31h0">
   </path><path d="M366 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="338" y="20">
   </rect><text x="352" y="35">
   )</text></g><path d="M366 31h10">
   </path></g><path d="M380 31h20">
   </path><path d="M160 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M180 61h0">
   </path><path d="M380 61h0">
   </path><path d="M180 61h10">
   </path><g class="terminal">
   <path d="M190 61h0">
   </path><path d="M274 61h0">
   </path><rect height="22" rx="10" ry="10" width="84" x="190" y="50">
   </rect><text x="232" y="65">
   getState</text></g><path d="M274 61h10">
   </path><path d="M284 61h10">
   </path><g class="terminal">
   <path d="M294 61h0">
   </path><path d="M322 61h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="294" y="50">
   </rect><text x="308" y="65">
   (</text></g><path d="M322 61h10">
   </path><path d="M332 61h10">
   </path><g class="terminal">
   <path d="M342 61h0">
   </path><path d="M370 61h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="342" y="50">
   </rect><text x="356" y="65">
   )</text></g><path d="M370 61h10">
   </path></g><path d="M380 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g></g><path d="M 400 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

guard
-----

.. raw:: html

   <svg class="railroad-diagram" height="132" viewBox="0 0 517 132" width="517" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M476 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M78 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="50" y="30">
   </rect><text x="64" y="45">
   :</text></g><path d="M78 41h10">
   </path><g>
   <path d="M88 41h0">
   </path><path d="M476 41h0">
   </path><path d="M88 41h20">
   </path><g>
   <path d="M108 41h0">
   </path><path d="M456 41h0">
   </path><path d="M108 41h10">
   </path><g class="terminal">
   <path d="M118 41h0">
   </path><path d="M218 41h0">
   </path><rect height="22" rx="10" ry="10" width="100" x="118" y="30">
   </rect><text x="168" y="45">
   IDENTIFIER</text></g><path d="M218 41h10">
   </path><g>
   <path d="M228 41h0">
   </path><path d="M456 41h0">
   </path><path d="M228 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M248 21h188">
   </path></g><path d="M436 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M228 41h20">
   </path><g>
   <path d="M248 41h0">
   </path><path d="M436 41h0">
   </path><path d="M248 41h10">
   </path><g class="terminal">
   <path d="M258 41h0">
   </path><path d="M286 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="258" y="30">
   </rect><text x="272" y="45">
   [</text></g><path d="M286 41h10">
   </path><path d="M296 41h10">
   </path><g>
   <path d="M306 41h0">
   </path><path d="M378 41h0">
   </path><path d="M306 41h10">
   </path><g class="non-terminal">
   <path d="M316 41h0">
   </path><path d="M368 41h0">
   </path><rect height="22" width="52" x="316" y="30">
   </rect><text x="342" y="45">
   expr</text></g><path d="M368 41h10">
   </path><path d="M316 41a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M316 71h12">
   </path><path d="M356 71h12">
   </path><rect height="22" rx="10" ry="10" width="28" x="328" y="60">
   </rect><text x="342" y="75">
   ,</text></g><path d="M368 71a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M378 41h10">
   </path><path d="M388 41h10">
   </path><g class="terminal">
   <path d="M398 41h0">
   </path><path d="M426 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="398" y="30">
   </rect><text x="412" y="45">
   ]</text></g><path d="M426 41h10">
   </path></g><path d="M436 41h20">
   </path></g></g><path d="M456 41h20">
   </path><path d="M88 41a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g>
   <path d="M108 101h90">
   </path><path d="M366 101h90">
   </path><path d="M198 101h10">
   </path><g class="terminal">
   <path d="M208 101h0">
   </path><path d="M236 101h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="208" y="90">
   </rect><text x="222" y="105">
   (</text></g><path d="M236 101h10">
   </path><path d="M246 101h10">
   </path><g class="non-terminal">
   <path d="M256 101h0">
   </path><path d="M308 101h0">
   </path><rect height="22" width="52" x="256" y="90">
   </rect><text x="282" y="105">
   expr</text></g><path d="M308 101h10">
   </path><path d="M318 101h10">
   </path><g class="terminal">
   <path d="M328 101h0">
   </path><path d="M356 101h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="328" y="90">
   </rect><text x="342" y="105">
   )</text></g><path d="M356 101h10">
   </path></g><path d="M456 101a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path></g></g><path d="M 476 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

expr
----

.. raw:: html

   <svg class="railroad-diagram" height="152" viewBox="0 0 381 152" width="381" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M340 31h0">
   </path><path d="M40 31h20">
   </path><g>
   <path d="M60 31h0">
   </path><path d="M320 31h0">
   </path><g>
   <path d="M60 31h0">
   </path><path d="M184 31h0">
   </path><path d="M60 31h20">
   </path><g class="terminal">
   <path d="M80 31h0">
   </path><path d="M164 31h0">
   </path><rect height="22" rx="10" ry="10" width="84" x="80" y="20">
   </rect><text x="122" y="35">
   continue</text></g><path d="M164 31h20">
   </path><path d="M60 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M80 61h12">
   </path><path d="M152 61h12">
   </path><rect height="22" rx="10" ry="10" width="60" x="92" y="50">
   </rect><text x="122" y="65">
   break</text></g><path d="M164 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M60 31a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M80 91h8">
   </path><path d="M156 91h8">
   </path><rect height="22" rx="10" ry="10" width="68" x="88" y="80">
   </rect><text x="122" y="95">
   return</text></g><path d="M164 91a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M184 31h0">
   </path><path d="M320 31h0">
   </path><path d="M184 31h20">
   </path><g>
   <path d="M204 31h0">
   </path><path d="M300 31h0">
   </path><path d="M204 31h10">
   </path><g class="terminal">
   <path d="M214 31h0">
   </path><path d="M242 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="214" y="20">
   </rect><text x="228" y="35">
   (</text></g><path d="M242 31h10">
   </path><path d="M252 31h10">
   </path><g class="terminal">
   <path d="M262 31h0">
   </path><path d="M290 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="262" y="20">
   </rect><text x="276" y="35">
   )</text></g><path d="M290 31h10">
   </path></g><path d="M300 31h20">
   </path><path d="M184 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M204 61h34">
   </path><path d="M266 61h34">
   </path><rect height="22" rx="10" ry="10" width="28" x="238" y="50">
   </rect><text x="252" y="65">
   ;</text></g><path d="M300 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M184 31a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M204 91h2">
   </path><path d="M298 91h2">
   </path><rect height="22" width="92" x="206" y="80">
   </rect><text x="252" y="95">
   blockExpr</text></g><path d="M300 91a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path></g></g><path d="M320 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 121h96">
   </path><path d="M224 121h96">
   </path><rect height="22" width="68" x="156" y="110">
   </rect><text x="190" y="125">
   assign</text></g><path d="M320 121a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path></g><path d="M 340 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

assign
------

.. raw:: html

   <svg class="railroad-diagram" height="222" viewBox="0 0 657 222" width="657" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M616 41h0">
   </path><path d="M40 41h20">
   </path><g>
   <path d="M60 41h0">
   </path><path d="M596 41h0">
   </path><path d="M60 41h10">
   </path><g class="terminal">
   <path d="M70 41h0">
   </path><path d="M114 41h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="70" y="30">
   </rect><text x="92" y="45">
   def</text></g><path d="M114 41h10">
   </path><path d="M124 41h10">
   </path><g class="non-terminal">
   <path d="M134 41h0">
   </path><path d="M210 41h0">
   </path><rect height="22" width="76" x="134" y="30">
   </rect><text x="172" y="45">
   pattern</text></g><path d="M210 41h10">
   </path><g>
   <path d="M220 41h0">
   </path><path d="M412 41h0">
   </path><path d="M220 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M240 21h152">
   </path></g><path d="M392 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M220 41h20">
   </path><g>
   <path d="M240 41h0">
   </path><path d="M392 41h0">
   </path><path d="M240 41h10">
   </path><g class="terminal">
   <path d="M250 41h0">
   </path><path d="M302 41h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="250" y="30">
   </rect><text x="276" y="45">
   exit</text></g><path d="M302 41h10">
   </path><path d="M312 41h10">
   </path><g class="non-terminal">
   <path d="M322 41h0">
   </path><path d="M382 41h0">
   </path><rect height="22" width="60" x="322" y="30">
   </rect><text x="352" y="45">
   order</text></g><path d="M382 41h10">
   </path></g><path d="M392 41h20">
   </path></g><g>
   <path d="M412 41h0">
   </path><path d="M596 41h0">
   </path><path d="M412 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M432 21h144">
   </path></g><path d="M576 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M412 41h20">
   </path><g>
   <path d="M432 41h0">
   </path><path d="M576 41h0">
   </path><path d="M432 41h10">
   </path><g class="terminal">
   <path d="M442 41h0">
   </path><path d="M478 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="442" y="30">
   </rect><text x="460" y="45">
   :=</text></g><path d="M478 41h10">
   </path><path d="M488 41h10">
   </path><g class="non-terminal">
   <path d="M498 41h0">
   </path><path d="M566 41h0">
   </path><rect height="22" width="68" x="498" y="30">
   </rect><text x="532" y="45">
   assign</text></g><path d="M566 41h10">
   </path></g><path d="M576 41h20">
   </path></g></g><path d="M596 41h20">
   </path><path d="M40 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 71h102">
   </path><path d="M494 71h102">
   </path><g>
   <path d="M162 71h0">
   </path><path d="M254 71h0">
   </path><path d="M162 71h20">
   </path><g class="terminal">
   <path d="M182 71h4">
   </path><path d="M230 71h4">
   </path><rect height="22" rx="10" ry="10" width="44" x="186" y="60">
   </rect><text x="208" y="75">
   var</text></g><path d="M234 71h20">
   </path><path d="M162 71a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M182 101h0">
   </path><path d="M234 101h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="182" y="90">
   </rect><text x="208" y="105">
   bind</text></g><path d="M234 101a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M254 71h10">
   </path><g class="non-terminal">
   <path d="M264 71h0">
   </path><path d="M340 71h0">
   </path><rect height="22" width="76" x="264" y="60">
   </rect><text x="302" y="75">
   pattern</text></g><path d="M340 71h10">
   </path><path d="M350 71h10">
   </path><g class="terminal">
   <path d="M360 71h0">
   </path><path d="M396 71h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="360" y="60">
   </rect><text x="378" y="75">
   :=</text></g><path d="M396 71h10">
   </path><path d="M406 71h10">
   </path><g class="non-terminal">
   <path d="M416 71h0">
   </path><path d="M484 71h0">
   </path><rect height="22" width="68" x="416" y="60">
   </rect><text x="450" y="75">
   assign</text></g><path d="M484 71h10">
   </path></g><path d="M596 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 131h160">
   </path><path d="M436 131h160">
   </path><path d="M220 131h10">
   </path><g class="non-terminal">
   <path d="M230 131h0">
   </path><path d="M282 131h0">
   </path><rect height="22" width="52" x="230" y="120">
   </rect><text x="256" y="135">
   lval</text></g><path d="M282 131h10">
   </path><path d="M292 131h10">
   </path><g class="terminal">
   <path d="M302 131h0">
   </path><path d="M338 131h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="302" y="120">
   </rect><text x="320" y="135">
   :=</text></g><path d="M338 131h10">
   </path><path d="M348 131h10">
   </path><g class="non-terminal">
   <path d="M358 131h0">
   </path><path d="M426 131h0">
   </path><rect height="22" width="68" x="358" y="120">
   </rect><text x="392" y="135">
   assign</text></g><path d="M426 131h10">
   </path></g><path d="M596 131a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v100a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 161h228">
   </path><path d="M368 161h228">
   </path><text class="comment" x="328" y="166">
   @op=...XXX</text></g><path d="M596 161a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v130a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 191h210">
   </path><path d="M385 191h210">
   </path><text class="comment" x="328" y="196">
   VERB_ASSIGN XXX</text></g><path d="M596 191a10 10 0 0 0 10 -10v-130a10 10 0 0 1 10 -10">
   </path></g><path d="M 616 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

lval
----

.. raw:: html

   <svg class="railroad-diagram" height="92" viewBox="0 0 197 92" width="197" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M156 31h0">
   </path><path d="M40 31h20">
   </path><g class="non-terminal">
   <path d="M60 31h12">
   </path><path d="M124 31h12">
   </path><rect height="22" width="52" x="72" y="20">
   </rect><text x="98" y="35">
   noun</text></g><path d="M136 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 61h0">
   </path><path d="M136 61h0">
   </path><rect height="22" width="76" x="60" y="50">
   </rect><text x="98" y="65">
   getExpr</text></g><path d="M136 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M 156 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

infix
-----

.. raw:: html

   <svg class="railroad-diagram" height="102" viewBox="0 0 349 102" width="349" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M308 41h0">
   </path><path d="M40 41h10">
   </path><g class="non-terminal">
   <path d="M50 41h0">
   </path><path d="M102 41h0">
   </path><rect height="22" width="52" x="50" y="30">
   </rect><text x="76" y="45">
   comp</text></g><path d="M102 41h10">
   </path><g>
   <path d="M112 41h0">
   </path><path d="M308 41h0">
   </path><path d="M112 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M132 21h156">
   </path></g><path d="M288 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M112 41h20">
   </path><g>
   <path d="M132 41h0">
   </path><path d="M288 41h0">
   </path><g>
   <path d="M132 41h0">
   </path><path d="M208 41h0">
   </path><path d="M132 41h20">
   </path><g class="terminal">
   <path d="M152 41h0">
   </path><path d="M188 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="152" y="30">
   </rect><text x="170" y="45">
   ||</text></g><path d="M188 41h20">
   </path><path d="M132 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M152 71h0">
   </path><path d="M188 71h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="152" y="60">
   </rect><text x="170" y="75">
   &amp;&amp;</text></g><path d="M188 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M208 41h10">
   </path><g class="non-terminal">
   <path d="M218 41h0">
   </path><path d="M278 41h0">
   </path><rect height="22" width="60" x="218" y="30">
   </rect><text x="248" y="45">
   infix</text></g><path d="M278 41h10">
   </path></g><path d="M288 41h20">
   </path></g></g><path d="M 308 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

comp
----

.. raw:: html

   <svg class="railroad-diagram" height="282" viewBox="0 0 349 282" width="349" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><path d="M40 41h10">
   </path><g class="non-terminal">
   <path d="M50 41h0">
   </path><path d="M110 41h0">
   </path><rect height="22" width="60" x="50" y="30">
   </rect><text x="80" y="45">
   order</text></g><path d="M110 41h10">
   </path><g>
   <path d="M120 41h0">
   </path><path d="M308 41h0">
   </path><path d="M120 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M140 21h148">
   </path></g><path d="M288 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M120 41h20">
   </path><g>
   <path d="M140 41h0">
   </path><path d="M288 41h0">
   </path><g>
   <path d="M140 41h0">
   </path><path d="M216 41h0">
   </path><path d="M140 41h20">
   </path><g class="terminal">
   <path d="M160 41h0">
   </path><path d="M196 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="160" y="30">
   </rect><text x="178" y="45">
   =~</text></g><path d="M196 41h20">
   </path><path d="M140 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M160 71h0">
   </path><path d="M196 71h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="160" y="60">
   </rect><text x="178" y="75">
   !~</text></g><path d="M196 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M140 41a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M160 101h0">
   </path><path d="M196 101h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="160" y="90">
   </rect><text x="178" y="105">
   ==</text></g><path d="M196 101a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path><path d="M140 41a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M160 131h0">
   </path><path d="M196 131h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="160" y="120">
   </rect><text x="178" y="135">
   !=</text></g><path d="M196 131a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path><path d="M140 41a10 10 0 0 1 10 10v100a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M160 161h0">
   </path><path d="M196 161h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="160" y="150">
   </rect><text x="178" y="165">
   &amp;!</text></g><path d="M196 161a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path><path d="M140 41a10 10 0 0 1 10 10v130a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M160 191h4">
   </path><path d="M192 191h4">
   </path><rect height="22" rx="10" ry="10" width="28" x="164" y="180">
   </rect><text x="178" y="195">
   ^</text></g><path d="M196 191a10 10 0 0 0 10 -10v-130a10 10 0 0 1 10 -10">
   </path><path d="M140 41a10 10 0 0 1 10 10v160a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M160 221h4">
   </path><path d="M192 221h4">
   </path><rect height="22" rx="10" ry="10" width="28" x="164" y="210">
   </rect><text x="178" y="225">
   &amp;</text></g><path d="M196 221a10 10 0 0 0 10 -10v-160a10 10 0 0 1 10 -10">
   </path><path d="M140 41a10 10 0 0 1 10 10v190a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M160 251h4">
   </path><path d="M192 251h4">
   </path><rect height="22" rx="10" ry="10" width="28" x="164" y="240">
   </rect><text x="178" y="255">
   |</text></g><path d="M196 251a10 10 0 0 0 10 -10v-190a10 10 0 0 1 10 -10">
   </path></g><path d="M216 41h10">
   </path><g class="non-terminal">
   <path d="M226 41h0">
   </path><path d="M278 41h0">
   </path><rect height="22" width="52" x="226" y="30">
   </rect><text x="252" y="45">
   comp</text></g><path d="M278 41h10">
   </path></g><path d="M288 41h20">
   </path></g><path d="M 308 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

order
-----

.. raw:: html

   <svg class="railroad-diagram" height="522" viewBox="0 0 373 522" width="373" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><path d="M40 41h10">
   </path><g class="non-terminal">
   <path d="M50 41h0">
   </path><path d="M118 41h0">
   </path><rect height="22" width="68" x="50" y="30">
   </rect><text x="84" y="45">
   prefix</text></g><path d="M118 41h10">
   </path><g>
   <path d="M128 41h0">
   </path><path d="M332 41h0">
   </path><path d="M128 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M148 21h164">
   </path></g><path d="M312 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M128 41h20">
   </path><g>
   <path d="M148 41h0">
   </path><path d="M312 41h0">
   </path><g>
   <path d="M148 41h0">
   </path><path d="M232 41h0">
   </path><path d="M148 41h20">
   </path><g class="terminal">
   <path d="M168 41h4">
   </path><path d="M208 41h4">
   </path><rect height="22" rx="10" ry="10" width="36" x="172" y="30">
   </rect><text x="190" y="45">
   **</text></g><path d="M212 41h20">
   </path><path d="M148 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 71h8">
   </path><path d="M204 71h8">
   </path><rect height="22" rx="10" ry="10" width="28" x="176" y="60">
   </rect><text x="190" y="75">
   *</text></g><path d="M212 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 101h8">
   </path><path d="M204 101h8">
   </path><rect height="22" rx="10" ry="10" width="28" x="176" y="90">
   </rect><text x="190" y="105">
   /</text></g><path d="M212 101a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 131h4">
   </path><path d="M208 131h4">
   </path><rect height="22" rx="10" ry="10" width="36" x="172" y="120">
   </rect><text x="190" y="135">
   //</text></g><path d="M212 131a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v100a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 161h8">
   </path><path d="M204 161h8">
   </path><rect height="22" rx="10" ry="10" width="28" x="176" y="150">
   </rect><text x="190" y="165">
   %</text></g><path d="M212 161a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v130a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 191h8">
   </path><path d="M204 191h8">
   </path><rect height="22" rx="10" ry="10" width="28" x="176" y="180">
   </rect><text x="190" y="195">
   +</text></g><path d="M212 191a10 10 0 0 0 10 -10v-130a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v160a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 221h8">
   </path><path d="M204 221h8">
   </path><rect height="22" rx="10" ry="10" width="28" x="176" y="210">
   </rect><text x="190" y="225">
   -</text></g><path d="M212 221a10 10 0 0 0 10 -10v-160a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v190a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 251h4">
   </path><path d="M208 251h4">
   </path><rect height="22" rx="10" ry="10" width="36" x="172" y="240">
   </rect><text x="190" y="255">
   &lt;&lt;</text></g><path d="M212 251a10 10 0 0 0 10 -10v-190a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v220a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 281h4">
   </path><path d="M208 281h4">
   </path><rect height="22" rx="10" ry="10" width="36" x="172" y="270">
   </rect><text x="190" y="285">
   >></text></g><path d="M212 281a10 10 0 0 0 10 -10v-220a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v250a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 311h4">
   </path><path d="M208 311h4">
   </path><rect height="22" rx="10" ry="10" width="36" x="172" y="300">
   </rect><text x="190" y="315">
   ..</text></g><path d="M212 311a10 10 0 0 0 10 -10v-250a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v280a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 341h0">
   </path><path d="M212 341h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="168" y="330">
   </rect><text x="190" y="345">
   ..!</text></g><path d="M212 341a10 10 0 0 0 10 -10v-280a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v310a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 371h8">
   </path><path d="M204 371h8">
   </path><rect height="22" rx="10" ry="10" width="28" x="176" y="360">
   </rect><text x="190" y="375">
   ></text></g><path d="M212 371a10 10 0 0 0 10 -10v-310a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v340a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 401h8">
   </path><path d="M204 401h8">
   </path><rect height="22" rx="10" ry="10" width="28" x="176" y="390">
   </rect><text x="190" y="405">
   &lt;</text></g><path d="M212 401a10 10 0 0 0 10 -10v-340a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v370a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 431h4">
   </path><path d="M208 431h4">
   </path><rect height="22" rx="10" ry="10" width="36" x="172" y="420">
   </rect><text x="190" y="435">
   >=</text></g><path d="M212 431a10 10 0 0 0 10 -10v-370a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v400a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 461h4">
   </path><path d="M208 461h4">
   </path><rect height="22" rx="10" ry="10" width="36" x="172" y="450">
   </rect><text x="190" y="465">
   &lt;=</text></g><path d="M212 461a10 10 0 0 0 10 -10v-400a10 10 0 0 1 10 -10">
   </path><path d="M148 41a10 10 0 0 1 10 10v430a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M168 491h0">
   </path><path d="M212 491h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="168" y="480">
   </rect><text x="190" y="495">
   &lt;=></text></g><path d="M212 491a10 10 0 0 0 10 -10v-430a10 10 0 0 1 10 -10">
   </path></g><path d="M232 41h10">
   </path><g class="non-terminal">
   <path d="M242 41h0">
   </path><path d="M302 41h0">
   </path><rect height="22" width="60" x="242" y="30">
   </rect><text x="272" y="45">
   order</text></g><path d="M302 41h10">
   </path></g><path d="M312 41h20">
   </path></g><path d="M 332 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

prefix
------

.. raw:: html

   <svg class="railroad-diagram" height="222" viewBox="0 0 293 222" width="293" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M252 31h0">
   </path><path d="M40 31h20">
   </path><g>
   <path d="M60 31h26">
   </path><path d="M206 31h26">
   </path><path d="M86 31h10">
   </path><g class="terminal">
   <path d="M96 31h0">
   </path><path d="M124 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="96" y="20">
   </rect><text x="110" y="35">
   -</text></g><path d="M124 31h10">
   </path><path d="M134 31h10">
   </path><g class="non-terminal">
   <path d="M144 31h0">
   </path><path d="M196 31h0">
   </path><rect height="22" width="52" x="144" y="20">
   </rect><text x="170" y="35">
   prim</text></g><path d="M196 31h10">
   </path></g><path d="M232 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 61h16">
   </path><path d="M216 61h16">
   </path><g>
   <path d="M76 61h0">
   </path><path d="M144 61h0">
   </path><path d="M76 61h20">
   </path><g class="terminal">
   <path d="M96 61h0">
   </path><path d="M124 61h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="96" y="50">
   </rect><text x="110" y="65">
   ~</text></g><path d="M124 61h20">
   </path><path d="M76 61a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M96 91h0">
   </path><path d="M124 91h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="96" y="80">
   </rect><text x="110" y="95">
   !</text></g><path d="M124 91a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M144 61h10">
   </path><g class="non-terminal">
   <path d="M154 61h0">
   </path><path d="M206 61h0">
   </path><rect height="22" width="52" x="154" y="50">
   </rect><text x="180" y="65">
   call</text></g><path d="M206 61h10">
   </path></g><path d="M232 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 121h26">
   </path><path d="M206 121h26">
   </path><path d="M86 121h10">
   </path><g class="terminal">
   <path d="M96 121h0">
   </path><path d="M124 121h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="96" y="110">
   </rect><text x="110" y="125">
   &amp;</text></g><path d="M124 121h10">
   </path><path d="M134 121h10">
   </path><g class="non-terminal">
   <path d="M144 121h0">
   </path><path d="M196 121h0">
   </path><rect height="22" width="52" x="144" y="110">
   </rect><text x="170" y="125">
   noun</text></g><path d="M196 121h10">
   </path></g><path d="M232 121a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v100a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 151h22">
   </path><path d="M210 151h22">
   </path><path d="M82 151h10">
   </path><g class="terminal">
   <path d="M92 151h0">
   </path><path d="M128 151h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="92" y="140">
   </rect><text x="110" y="155">
   &amp;&amp;</text></g><path d="M128 151h10">
   </path><path d="M138 151h10">
   </path><g class="non-terminal">
   <path d="M148 151h0">
   </path><path d="M200 151h0">
   </path><rect height="22" width="52" x="148" y="140">
   </rect><text x="174" y="155">
   noun</text></g><path d="M200 151h10">
   </path></g><path d="M232 151a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v140a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 191h0">
   </path><path d="M232 191h0">
   </path><path d="M60 191h10">
   </path><g class="non-terminal">
   <path d="M70 191h0">
   </path><path d="M122 191h0">
   </path><rect height="22" width="52" x="70" y="180">
   </rect><text x="96" y="195">
   call</text></g><path d="M122 191h10">
   </path><g>
   <path d="M132 191h0">
   </path><path d="M232 191h0">
   </path><path d="M132 191a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M152 171h60">
   </path></g><path d="M212 171a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M132 191h20">
   </path><g class="non-terminal">
   <path d="M152 191h0">
   </path><path d="M212 191h0">
   </path><rect height="22" width="60" x="152" y="180">
   </rect><text x="182" y="195">
   guard</text></g><path d="M212 191h20">
   </path></g></g><path d="M232 191a10 10 0 0 0 10 -10v-140a10 10 0 0 1 10 -10">
   </path></g><path d="M 252 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

call
----

.. raw:: html

   <svg class="railroad-diagram" height="72" viewBox="0 0 281 72" width="281" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M240 41h0">
   </path><path d="M40 41h10">
   </path><g class="non-terminal">
   <path d="M50 41h0">
   </path><path d="M110 41h0">
   </path><rect height="22" width="60" x="50" y="30">
   </rect><text x="80" y="45">
   calls</text></g><path d="M110 41h10">
   </path><g>
   <path d="M120 41h0">
   </path><path d="M240 41h0">
   </path><path d="M120 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M140 21h80">
   </path></g><path d="M220 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M120 41h20">
   </path><g>
   <path d="M140 41h0">
   </path><path d="M220 41h0">
   </path><path d="M140 41h10">
   </path><g class="non-terminal">
   <path d="M150 41h0">
   </path><path d="M210 41h0">
   </path><rect height="22" width="60" x="150" y="30">
   </rect><text x="180" y="45">
   curry</text></g><path d="M210 41h10">
   </path></g><path d="M220 41h20">
   </path></g></g><path d="M 240 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

calls
-----

.. raw:: html

   <svg class="railroad-diagram" height="162" viewBox="0 0 665 162" width="665" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M624 31h0">
   </path><path d="M40 31h20">
   </path><g class="non-terminal">
   <path d="M60 31h246">
   </path><path d="M358 31h246">
   </path><rect height="22" width="52" x="306" y="20">
   </rect><text x="332" y="35">
   prim</text></g><path d="M604 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v20a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 71h0">
   </path><path d="M604 71h0">
   </path><path d="M60 71h10">
   </path><g class="non-terminal">
   <path d="M70 71h0">
   </path><path d="M130 71h0">
   </path><rect height="22" width="60" x="70" y="60">
   </rect><text x="100" y="75">
   calls</text></g><path d="M130 71h10">
   </path><g>
   <path d="M140 71h0">
   </path><path d="M396 71h0">
   </path><path d="M140 71a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M160 51h216">
   </path></g><path d="M376 51a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M140 71h20">
   </path><g>
   <path d="M160 71h0">
   </path><path d="M376 71h0">
   </path><g>
   <path d="M160 71h0">
   </path><path d="M236 71h0">
   </path><path d="M160 71h20">
   </path><g class="terminal">
   <path d="M180 71h4">
   </path><path d="M212 71h4">
   </path><rect height="22" rx="10" ry="10" width="28" x="184" y="60">
   </rect><text x="198" y="75">
   .</text></g><path d="M216 71h20">
   </path><path d="M160 71a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M180 101h0">
   </path><path d="M216 101h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="180" y="90">
   </rect><text x="198" y="105">
   &lt;-</text></g><path d="M216 101a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M236 71h0">
   </path><path d="M376 71h0">
   </path><path d="M236 71h20">
   </path><g class="terminal">
   <path d="M256 71h0">
   </path><path d="M356 71h0">
   </path><rect height="22" rx="10" ry="10" width="100" x="256" y="60">
   </rect><text x="306" y="75">
   IDENTIFIER</text></g><path d="M356 71h20">
   </path><path d="M236 71a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M256 101h8">
   </path><path d="M348 101h8">
   </path><rect height="22" rx="10" ry="10" width="84" x="264" y="90">
   </rect><text x="306" y="105">
   .String.</text></g><path d="M356 101a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g></g><path d="M376 71h20">
   </path></g><g>
   <path d="M396 71h0">
   </path><path d="M604 71h0">
   </path><path d="M396 71h10">
   </path><g class="terminal">
   <path d="M406 71h0">
   </path><path d="M434 71h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="406" y="60">
   </rect><text x="420" y="75">
   (</text></g><path d="M434 71h10">
   </path><g>
   <path d="M444 71h0">
   </path><path d="M556 71h0">
   </path><path d="M444 71a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M464 51h72">
   </path></g><path d="M536 51a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M444 71h20">
   </path><g>
   <path d="M464 71h0">
   </path><path d="M536 71h0">
   </path><path d="M464 71h10">
   </path><g class="non-terminal">
   <path d="M474 71h0">
   </path><path d="M526 71h0">
   </path><rect height="22" width="52" x="474" y="60">
   </rect><text x="500" y="75">
   expr</text></g><path d="M526 71h10">
   </path><path d="M474 71a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M474 101h12">
   </path><path d="M514 101h12">
   </path><rect height="22" rx="10" ry="10" width="28" x="486" y="90">
   </rect><text x="500" y="105">
   ,</text></g><path d="M526 101a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M536 71h20">
   </path></g><path d="M556 71h10">
   </path><g class="terminal">
   <path d="M566 71h0">
   </path><path d="M594 71h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="566" y="60">
   </rect><text x="580" y="75">
   )</text></g><path d="M594 71h10">
   </path></g></g><path d="M604 71a10 10 0 0 0 10 -10v-20a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v80a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 131h234">
   </path><path d="M370 131h234">
   </path><rect height="22" width="76" x="294" y="120">
   </rect><text x="332" y="135">
   getExpr</text></g><path d="M604 131a10 10 0 0 0 10 -10v-80a10 10 0 0 1 10 -10">
   </path></g><path d="M 624 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

getExpr
-------

.. raw:: html

   <svg class="railroad-diagram" height="102" viewBox="0 0 369 102" width="369" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M328 41h0">
   </path><path d="M40 41h10">
   </path><g class="non-terminal">
   <path d="M50 41h0">
   </path><path d="M110 41h0">
   </path><rect height="22" width="60" x="50" y="30">
   </rect><text x="80" y="45">
   calls</text></g><path d="M110 41h10">
   </path><g>
   <path d="M120 41h0">
   </path><path d="M328 41h0">
   </path><path d="M120 41h10">
   </path><g class="terminal">
   <path d="M130 41h0">
   </path><path d="M158 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="130" y="30">
   </rect><text x="144" y="45">
   [</text></g><path d="M158 41h10">
   </path><g>
   <path d="M168 41h0">
   </path><path d="M280 41h0">
   </path><path d="M168 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M188 21h72">
   </path></g><path d="M260 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M168 41h20">
   </path><g>
   <path d="M188 41h0">
   </path><path d="M260 41h0">
   </path><path d="M188 41h10">
   </path><g class="non-terminal">
   <path d="M198 41h0">
   </path><path d="M250 41h0">
   </path><rect height="22" width="52" x="198" y="30">
   </rect><text x="224" y="45">
   expr</text></g><path d="M250 41h10">
   </path><path d="M198 41a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M198 71h12">
   </path><path d="M238 71h12">
   </path><rect height="22" rx="10" ry="10" width="28" x="210" y="60">
   </rect><text x="224" y="75">
   ,</text></g><path d="M250 71a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M260 41h20">
   </path></g><path d="M280 41h10">
   </path><g class="terminal">
   <path d="M290 41h0">
   </path><path d="M318 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="290" y="30">
   </rect><text x="304" y="45">
   ]</text></g><path d="M318 41h10">
   </path></g></g><path d="M 328 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

curry
-----

.. raw:: html

   <svg class="railroad-diagram" height="92" viewBox="0 0 297 92" width="297" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M256 31h0">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M116 31h0">
   </path><path d="M40 31h20">
   </path><g class="terminal">
   <path d="M60 31h4">
   </path><path d="M92 31h4">
   </path><rect height="22" rx="10" ry="10" width="28" x="64" y="20">
   </rect><text x="78" y="35">
   .</text></g><path d="M96 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M60 61h0">
   </path><path d="M96 61h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="60" y="50">
   </rect><text x="78" y="65">
   &lt;-</text></g><path d="M96 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M116 31h0">
   </path><path d="M256 31h0">
   </path><path d="M116 31h20">
   </path><g class="terminal">
   <path d="M136 31h0">
   </path><path d="M236 31h0">
   </path><rect height="22" rx="10" ry="10" width="100" x="136" y="20">
   </rect><text x="186" y="35">
   IDENTIFIER</text></g><path d="M236 31h20">
   </path><path d="M116 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M136 61h8">
   </path><path d="M228 61h8">
   </path><rect height="22" rx="10" ry="10" width="84" x="144" y="50">
   </rect><text x="186" y="65">
   .String.</text></g><path d="M236 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g></g><path d="M 256 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

prim
----

.. raw:: html

   <svg class="railroad-diagram" height="521" viewBox="0 0 477 521" width="477" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M436 31h0">
   </path><path d="M40 31h20">
   </path><g class="terminal">
   <path d="M60 31h136">
   </path><path d="M280 31h136">
   </path><rect height="22" rx="10" ry="10" width="84" x="196" y="20">
   </rect><text x="238" y="35">
   .String.</text></g><path d="M416 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M60 61h148">
   </path><path d="M268 61h148">
   </path><rect height="22" rx="10" ry="10" width="60" x="208" y="50">
   </rect><text x="238" y="65">
   .int.</text></g><path d="M416 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M60 91h132">
   </path><path d="M284 91h132">
   </path><rect height="22" rx="10" ry="10" width="92" x="192" y="80">
   </rect><text x="238" y="95">
   .float64.</text></g><path d="M416 91a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M60 121h144">
   </path><path d="M272 121h144">
   </path><rect height="22" rx="10" ry="10" width="68" x="204" y="110">
   </rect><text x="238" y="125">
   .char.</text></g><path d="M416 121a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v100a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 151h120">
   </path><path d="M296 151h120">
   </path><rect height="22" width="116" x="180" y="140">
   </rect><text x="238" y="155">
   quasiliteral</text></g><path d="M416 151a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v130a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 181h78">
   </path><path d="M338 181h78">
   </path><path d="M138 181h20">
   </path><g class="terminal">
   <path d="M158 181h30">
   </path><path d="M288 181h30">
   </path><rect height="22" rx="10" ry="10" width="100" x="188" y="170">
   </rect><text x="238" y="185">
   IDENTIFIER</text></g><path d="M318 181h20">
   </path><path d="M138 181a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M158 211h0">
   </path><path d="M318 211h0">
   </path><path d="M158 211h10">
   </path><g class="terminal">
   <path d="M168 211h0">
   </path><path d="M204 211h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="168" y="200">
   </rect><text x="186" y="215">
   ::</text></g><path d="M204 211h10">
   </path><path d="M214 211h10">
   </path><g class="terminal">
   <path d="M224 211h0">
   </path><path d="M308 211h0">
   </path><rect height="22" rx="10" ry="10" width="84" x="224" y="200">
   </rect><text x="266" y="215">
   .String.</text></g><path d="M308 211h10">
   </path></g><path d="M318 211a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M416 181a10 10 0 0 0 10 -10v-130a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v190a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 241h94">
   </path><path d="M322 241h94">
   </path><path d="M154 241h10">
   </path><g class="terminal">
   <path d="M164 241h0">
   </path><path d="M192 241h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="164" y="230">
   </rect><text x="178" y="245">
   (</text></g><path d="M192 241h10">
   </path><path d="M202 241h10">
   </path><g class="non-terminal">
   <path d="M212 241h0">
   </path><path d="M264 241h0">
   </path><rect height="22" width="52" x="212" y="230">
   </rect><text x="238" y="245">
   expr</text></g><path d="M264 241h10">
   </path><path d="M274 241h10">
   </path><g class="terminal">
   <path d="M284 241h0">
   </path><path d="M312 241h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="284" y="230">
   </rect><text x="298" y="245">
   )</text></g><path d="M312 241h10">
   </path></g><path d="M416 241a10 10 0 0 0 10 -10v-190a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v230a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 281h74">
   </path><path d="M342 281h74">
   </path><path d="M134 281h10">
   </path><g class="terminal">
   <path d="M144 281h0">
   </path><path d="M172 281h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="144" y="270">
   </rect><text x="158" y="285">
   {</text></g><path d="M172 281h10">
   </path><g>
   <path d="M182 281h0">
   </path><path d="M294 281h0">
   </path><path d="M182 281a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M202 261h72">
   </path></g><path d="M274 261a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M182 281h20">
   </path><g>
   <path d="M202 281h0">
   </path><path d="M274 281h0">
   </path><path d="M202 281h10">
   </path><g class="non-terminal">
   <path d="M212 281h0">
   </path><path d="M264 281h0">
   </path><rect height="22" width="52" x="212" y="270">
   </rect><text x="238" y="285">
   expr</text></g><path d="M264 281h10">
   </path><path d="M212 281a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M212 311h12">
   </path><path d="M252 311h12">
   </path><rect height="22" rx="10" ry="10" width="28" x="224" y="300">
   </rect><text x="238" y="315">
   ;</text></g><path d="M264 311a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M274 281h20">
   </path></g><path d="M294 281h10">
   </path><g class="terminal">
   <path d="M304 281h0">
   </path><path d="M332 281h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="304" y="270">
   </rect><text x="318" y="285">
   }</text></g><path d="M332 281h10">
   </path></g><path d="M416 281a10 10 0 0 0 10 -10v-230a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v290a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 341h0">
   </path><path d="M416 341h0">
   </path><path d="M60 341h10">
   </path><g class="terminal">
   <path d="M70 341h0">
   </path><path d="M98 341h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="70" y="330">
   </rect><text x="84" y="345">
   [</text></g><path d="M98 341h10">
   </path><g>
   <path d="M108 341h0">
   </path><path d="M368 341h0">
   </path><path d="M108 341h20">
   </path><g>
   <path d="M128 341h220">
   </path></g><path d="M348 341h20">
   </path><path d="M108 341a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><g>
   <path d="M128 361h74">
   </path><path d="M274 361h74">
   </path><path d="M202 361h10">
   </path><g class="non-terminal">
   <path d="M212 361h0">
   </path><path d="M264 361h0">
   </path><rect height="22" width="52" x="212" y="350">
   </rect><text x="238" y="365">
   expr</text></g><path d="M264 361h10">
   </path><path d="M212 361a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M212 391h12">
   </path><path d="M252 391h12">
   </path><rect height="22" rx="10" ry="10" width="28" x="224" y="380">
   </rect><text x="238" y="395">
   ,</text></g><path d="M264 391a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M348 361a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><path d="M108 341a10 10 0 0 1 10 10v60a10 10 0 0 0 10 10">
   </path><g>
   <path d="M128 421h0">
   </path><path d="M348 421h0">
   </path><path d="M128 421h10">
   </path><g>
   <path d="M138 421h0">
   </path><path d="M338 421h0">
   </path><path d="M138 421h10">
   </path><g class="non-terminal">
   <path d="M148 421h0">
   </path><path d="M200 421h0">
   </path><rect height="22" width="52" x="148" y="410">
   </rect><text x="174" y="425">
   expr</text></g><path d="M200 421h10">
   </path><path d="M210 421h10">
   </path><g class="terminal">
   <path d="M220 421h0">
   </path><path d="M256 421h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="220" y="410">
   </rect><text x="238" y="425">
   =></text></g><path d="M256 421h10">
   </path><path d="M266 421h10">
   </path><g class="non-terminal">
   <path d="M276 421h0">
   </path><path d="M328 421h0">
   </path><rect height="22" width="52" x="276" y="410">
   </rect><text x="302" y="425">
   expr</text></g><path d="M328 421h10">
   </path></g><path d="M338 421h10">
   </path><path d="M138 421a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M138 451h86">
   </path><path d="M252 451h86">
   </path><rect height="22" rx="10" ry="10" width="28" x="224" y="440">
   </rect><text x="238" y="455">
   ,</text></g><path d="M338 451a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M348 421a10 10 0 0 0 10 -10v-60a10 10 0 0 1 10 -10">
   </path><path d="M108 341a10 10 0 0 1 10 10v120a10 10 0 0 0 10 10">
   </path><g>
   <path d="M128 481h6">
   </path><path d="M342 481h6">
   </path><path d="M134 481h10">
   </path><g class="terminal">
   <path d="M144 481h0">
   </path><path d="M188 481h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="144" y="470">
   </rect><text x="166" y="485">
   for</text></g><path d="M188 481h10">
   </path><path d="M198 481h10">
   </path><g class="non-terminal">
   <path d="M208 481h0">
   </path><path d="M332 481h0">
   </path><rect height="22" width="124" x="208" y="470">
   </rect><text x="270" y="485">
   comprehension</text></g><path d="M332 481h10">
   </path></g><path d="M348 481a10 10 0 0 0 10 -10v-120a10 10 0 0 1 10 -10">
   </path></g><path d="M368 341h10">
   </path><g class="terminal">
   <path d="M378 341h0">
   </path><path d="M406 341h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="378" y="330">
   </rect><text x="392" y="345">
   ]</text></g><path d="M406 341h10">
   </path></g><path d="M416 341a10 10 0 0 0 10 -10v-290a10 10 0 0 1 10 -10">
   </path></g><path d="M 436 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

comprehension
-------------

.. raw:: html

   <svg class="railroad-diagram" height="92" viewBox="0 0 697 92" width="697" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M656 31h0">
   </path><path d="M40 31h20">
   </path><g>
   <path d="M60 31h140">
   </path><path d="M496 31h140">
   </path><path d="M200 31h10">
   </path><g class="non-terminal">
   <path d="M210 31h0">
   </path><path d="M286 31h0">
   </path><rect height="22" width="76" x="210" y="20">
   </rect><text x="248" y="35">
   pattern</text></g><path d="M286 31h10">
   </path><path d="M296 31h10">
   </path><g class="terminal">
   <path d="M306 31h0">
   </path><path d="M342 31h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="306" y="20">
   </rect><text x="324" y="35">
   in</text></g><path d="M342 31h10">
   </path><path d="M352 31h10">
   </path><g class="non-terminal">
   <path d="M362 31h0">
   </path><path d="M414 31h0">
   </path><rect height="22" width="52" x="362" y="20">
   </rect><text x="388" y="35">
   iter</text></g><path d="M414 31h10">
   </path><path d="M424 31h10">
   </path><g class="non-terminal">
   <path d="M434 31h0">
   </path><path d="M486 31h0">
   </path><rect height="22" width="52" x="434" y="20">
   </rect><text x="460" y="35">
   expr</text></g><path d="M486 31h10">
   </path></g><path d="M636 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 61h0">
   </path><path d="M636 61h0">
   </path><path d="M60 61h10">
   </path><g class="non-terminal">
   <path d="M70 61h0">
   </path><path d="M146 61h0">
   </path><rect height="22" width="76" x="70" y="50">
   </rect><text x="108" y="65">
   pattern</text></g><path d="M146 61h10">
   </path><path d="M156 61h10">
   </path><g class="terminal">
   <path d="M166 61h0">
   </path><path d="M202 61h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="166" y="50">
   </rect><text x="184" y="65">
   =></text></g><path d="M202 61h10">
   </path><path d="M212 61h10">
   </path><g class="non-terminal">
   <path d="M222 61h0">
   </path><path d="M298 61h0">
   </path><rect height="22" width="76" x="222" y="50">
   </rect><text x="260" y="65">
   pattern</text></g><path d="M298 61h10">
   </path><path d="M308 61h10">
   </path><g class="terminal">
   <path d="M318 61h0">
   </path><path d="M354 61h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="318" y="50">
   </rect><text x="336" y="65">
   in</text></g><path d="M354 61h10">
   </path><path d="M364 61h10">
   </path><g class="non-terminal">
   <path d="M374 61h0">
   </path><path d="M426 61h0">
   </path><rect height="22" width="52" x="374" y="50">
   </rect><text x="400" y="65">
   iter</text></g><path d="M426 61h10">
   </path><path d="M436 61h10">
   </path><g class="non-terminal">
   <path d="M446 61h0">
   </path><path d="M498 61h0">
   </path><rect height="22" width="52" x="446" y="50">
   </rect><text x="472" y="65">
   expr</text></g><path d="M498 61h10">
   </path><path d="M508 61h10">
   </path><g class="terminal">
   <path d="M518 61h0">
   </path><path d="M554 61h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="518" y="50">
   </rect><text x="536" y="65">
   =></text></g><path d="M554 61h10">
   </path><path d="M564 61h10">
   </path><g class="non-terminal">
   <path d="M574 61h0">
   </path><path d="M626 61h0">
   </path><rect height="22" width="52" x="574" y="50">
   </rect><text x="600" y="65">
   expr</text></g><path d="M626 61h10">
   </path></g><path d="M636 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M 656 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

iter
----

.. raw:: html

   <svg class="railroad-diagram" height="72" viewBox="0 0 329 72" width="329" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M288 41h0">
   </path><path d="M40 41h10">
   </path><g class="non-terminal">
   <path d="M50 41h0">
   </path><path d="M110 41h0">
   </path><rect height="22" width="60" x="50" y="30">
   </rect><text x="80" y="45">
   order</text></g><path d="M110 41h10">
   </path><g>
   <path d="M120 41h0">
   </path><path d="M288 41h0">
   </path><path d="M120 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M140 21h128">
   </path></g><path d="M268 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M120 41h20">
   </path><g>
   <path d="M140 41h0">
   </path><path d="M268 41h0">
   </path><path d="M140 41h10">
   </path><g class="terminal">
   <path d="M150 41h0">
   </path><path d="M186 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="150" y="30">
   </rect><text x="168" y="45">
   if</text></g><path d="M186 41h10">
   </path><path d="M196 41h10">
   </path><g class="non-terminal">
   <path d="M206 41h0">
   </path><path d="M258 41h0">
   </path><rect height="22" width="52" x="206" y="30">
   </rect><text x="232" y="45">
   comp</text></g><path d="M258 41h10">
   </path></g><path d="M268 41h20">
   </path></g></g><path d="M 288 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

pattern
-------

.. raw:: html

   <svg class="railroad-diagram" height="372" viewBox="0 0 829 372" width="829" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M788 41h0">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M532 41h0">
   </path><path d="M40 41h20">
   </path><g class="non-terminal">
   <path d="M60 41h172">
   </path><path d="M340 41h172">
   </path><rect height="22" width="108" x="232" y="30">
   </rect><text x="286" y="45">
   namePattern</text></g><path d="M512 41h20">
   </path><path d="M40 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 71h168">
   </path><path d="M344 71h168">
   </path><rect height="22" width="116" x="228" y="60">
   </rect><text x="286" y="75">
   quasiLiteral</text></g><path d="M512 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 101h152">
   </path><path d="M360 101h152">
   </path><g>
   <path d="M212 101h0">
   </path><path d="M288 101h0">
   </path><path d="M212 101h20">
   </path><g class="terminal">
   <path d="M232 101h0">
   </path><path d="M268 101h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="232" y="90">
   </rect><text x="250" y="105">
   ==</text></g><path d="M268 101h20">
   </path><path d="M212 101a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M232 131h0">
   </path><path d="M268 131h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="232" y="120">
   </rect><text x="250" y="135">
   !=</text></g><path d="M268 131a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M288 101h10">
   </path><g class="non-terminal">
   <path d="M298 101h0">
   </path><path d="M350 101h0">
   </path><rect height="22" width="52" x="298" y="90">
   </rect><text x="324" y="105">
   prim</text></g><path d="M350 101h10">
   </path></g><path d="M512 101a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v110a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 171h152">
   </path><path d="M360 171h152">
   </path><path d="M212 171h10">
   </path><g class="terminal">
   <path d="M222 171h0">
   </path><path d="M250 171h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="222" y="160">
   </rect><text x="236" y="175">
   _</text></g><path d="M250 171h10">
   </path><g>
   <path d="M260 171h0">
   </path><path d="M360 171h0">
   </path><path d="M260 171a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M280 151h60">
   </path></g><path d="M340 151a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M260 171h20">
   </path><g class="non-terminal">
   <path d="M280 171h0">
   </path><path d="M340 171h0">
   </path><rect height="22" width="60" x="280" y="160">
   </rect><text x="310" y="175">
   guard</text></g><path d="M340 171h20">
   </path></g></g><path d="M512 171a10 10 0 0 0 10 -10v-110a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v140a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 201h62">
   </path><path d="M450 201h62">
   </path><path d="M122 201h10">
   </path><g class="terminal">
   <path d="M132 201h0">
   </path><path d="M176 201h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="132" y="190">
   </rect><text x="154" y="205">
   via</text></g><path d="M176 201h10">
   </path><path d="M186 201h10">
   </path><g class="terminal">
   <path d="M196 201h0">
   </path><path d="M224 201h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="196" y="190">
   </rect><text x="210" y="205">
   (</text></g><path d="M224 201h10">
   </path><path d="M234 201h10">
   </path><g class="non-terminal">
   <path d="M244 201h0">
   </path><path d="M296 201h0">
   </path><rect height="22" width="52" x="244" y="190">
   </rect><text x="270" y="205">
   expr</text></g><path d="M296 201h10">
   </path><path d="M306 201h10">
   </path><g class="terminal">
   <path d="M316 201h0">
   </path><path d="M344 201h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="316" y="190">
   </rect><text x="330" y="205">
   )</text></g><path d="M344 201h10">
   </path><path d="M354 201h10">
   </path><g class="non-terminal">
   <path d="M364 201h0">
   </path><path d="M440 201h0">
   </path><rect height="22" width="76" x="364" y="190">
   </rect><text x="402" y="205">
   pattern</text></g><path d="M440 201h10">
   </path></g><path d="M512 201a10 10 0 0 0 10 -10v-140a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v180a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 241h18">
   </path><path d="M494 241h18">
   </path><path d="M78 241h10">
   </path><g class="terminal">
   <path d="M88 241h0">
   </path><path d="M116 241h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="88" y="230">
   </rect><text x="102" y="245">
   [</text></g><path d="M116 241h10">
   </path><g>
   <path d="M126 241h0">
   </path><path d="M262 241h0">
   </path><path d="M126 241a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M146 221h96">
   </path></g><path d="M242 221a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M126 241h20">
   </path><g>
   <path d="M146 241h0">
   </path><path d="M242 241h0">
   </path><path d="M146 241h10">
   </path><g class="non-terminal">
   <path d="M156 241h0">
   </path><path d="M232 241h0">
   </path><rect height="22" width="76" x="156" y="230">
   </rect><text x="194" y="245">
   pattern</text></g><path d="M232 241h10">
   </path><path d="M156 241a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M156 271h24">
   </path><path d="M208 271h24">
   </path><rect height="22" rx="10" ry="10" width="28" x="180" y="260">
   </rect><text x="194" y="275">
   ,</text></g><path d="M232 271a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M242 241h20">
   </path></g><path d="M262 241h10">
   </path><g class="terminal">
   <path d="M272 241h0">
   </path><path d="M300 241h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="272" y="230">
   </rect><text x="286" y="245">
   ]</text></g><path d="M300 241h10">
   </path><g>
   <path d="M310 241h0">
   </path><path d="M494 241h0">
   </path><path d="M310 241a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M330 221h144">
   </path></g><path d="M474 221a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M310 241h20">
   </path><g>
   <path d="M330 241h0">
   </path><path d="M474 241h0">
   </path><path d="M330 241h10">
   </path><g class="terminal">
   <path d="M340 241h0">
   </path><path d="M368 241h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="340" y="230">
   </rect><text x="354" y="245">
   +</text></g><path d="M368 241h10">
   </path><path d="M378 241h10">
   </path><g class="non-terminal">
   <path d="M388 241h0">
   </path><path d="M464 241h0">
   </path><rect height="22" width="76" x="388" y="230">
   </rect><text x="426" y="245">
   pattern</text></g><path d="M464 241h10">
   </path></g><path d="M474 241h20">
   </path></g></g><path d="M512 241a10 10 0 0 0 10 -10v-180a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v250a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 311h0">
   </path><path d="M512 311h0">
   </path><path d="M60 311h10">
   </path><g class="terminal">
   <path d="M70 311h0">
   </path><path d="M98 311h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="70" y="300">
   </rect><text x="84" y="315">
   [</text></g><path d="M98 311h10">
   </path><path d="M108 311h10">
   </path><g>
   <path d="M118 311h0">
   </path><path d="M270 311h0">
   </path><path d="M118 311h10">
   </path><g class="non-terminal">
   <path d="M128 311h0">
   </path><path d="M260 311h0">
   </path><rect height="22" width="132" x="128" y="300">
   </rect><text x="194" y="315">
   mapPatternItem</text></g><path d="M260 311h10">
   </path><path d="M128 311a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M128 341h52">
   </path><path d="M208 341h52">
   </path><rect height="22" rx="10" ry="10" width="28" x="180" y="330">
   </rect><text x="194" y="345">
   ,</text></g><path d="M260 341a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M270 311h10">
   </path><path d="M280 311h10">
   </path><g class="terminal">
   <path d="M290 311h0">
   </path><path d="M318 311h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="290" y="300">
   </rect><text x="304" y="315">
   ]</text></g><path d="M318 311h10">
   </path><g>
   <path d="M328 311h0">
   </path><path d="M512 311h0">
   </path><path d="M328 311a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M348 291h144">
   </path></g><path d="M492 291a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M328 311h20">
   </path><g>
   <path d="M348 311h0">
   </path><path d="M492 311h0">
   </path><path d="M348 311h10">
   </path><g class="terminal">
   <path d="M358 311h0">
   </path><path d="M386 311h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="358" y="300">
   </rect><text x="372" y="315">
   |</text></g><path d="M386 311h10">
   </path><path d="M396 311h10">
   </path><g class="non-terminal">
   <path d="M406 311h0">
   </path><path d="M482 311h0">
   </path><rect height="22" width="76" x="406" y="300">
   </rect><text x="444" y="315">
   pattern</text></g><path d="M482 311h10">
   </path></g><path d="M492 311h20">
   </path></g></g><path d="M512 311a10 10 0 0 0 10 -10v-250a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M532 41h0">
   </path><path d="M788 41h0">
   </path><path d="M532 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M552 21h216">
   </path></g><path d="M768 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M532 41h20">
   </path><g>
   <path d="M552 41h0">
   </path><path d="M768 41h0">
   </path><path d="M552 41h10">
   </path><g class="terminal">
   <path d="M562 41h0">
   </path><path d="M590 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="562" y="30">
   </rect><text x="576" y="45">
   ?</text></g><path d="M590 41h10">
   </path><path d="M600 41h10">
   </path><g class="terminal">
   <path d="M610 41h0">
   </path><path d="M638 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="610" y="30">
   </rect><text x="624" y="45">
   (</text></g><path d="M638 41h10">
   </path><path d="M648 41h10">
   </path><g class="non-terminal">
   <path d="M658 41h0">
   </path><path d="M710 41h0">
   </path><rect height="22" width="52" x="658" y="30">
   </rect><text x="684" y="45">
   expr</text></g><path d="M710 41h10">
   </path><path d="M720 41h10">
   </path><g class="terminal">
   <path d="M730 41h0">
   </path><path d="M758 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="730" y="30">
   </rect><text x="744" y="45">
   )</text></g><path d="M758 41h10">
   </path></g><path d="M768 41h20">
   </path></g></g><path d="M 788 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

namePattern
-----------

.. raw:: html

   <svg class="railroad-diagram" height="252" viewBox="0 0 421 252" width="421" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M380 41h0">
   </path><path d="M40 41h20">
   </path><g>
   <path d="M60 41h0">
   </path><path d="M360 41h0">
   </path><g>
   <path d="M60 41h0">
   </path><path d="M260 41h0">
   </path><path d="M60 41h20">
   </path><g class="terminal">
   <path d="M80 41h30">
   </path><path d="M210 41h30">
   </path><rect height="22" rx="10" ry="10" width="100" x="110" y="30">
   </rect><text x="160" y="45">
   IDENTIFIER</text></g><path d="M240 41h20">
   </path><path d="M60 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M80 71h0">
   </path><path d="M240 71h0">
   </path><path d="M80 71h10">
   </path><g class="terminal">
   <path d="M90 71h0">
   </path><path d="M126 71h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="90" y="60">
   </rect><text x="108" y="75">
   ::</text></g><path d="M126 71h10">
   </path><path d="M136 71h10">
   </path><g class="terminal">
   <path d="M146 71h0">
   </path><path d="M230 71h0">
   </path><rect height="22" rx="10" ry="10" width="84" x="146" y="60">
   </rect><text x="188" y="75">
   .String.</text></g><path d="M230 71h10">
   </path></g><path d="M240 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M260 41h0">
   </path><path d="M360 41h0">
   </path><path d="M260 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M280 21h60">
   </path></g><path d="M340 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M260 41h20">
   </path><g class="non-terminal">
   <path d="M280 41h0">
   </path><path d="M340 41h0">
   </path><rect height="22" width="60" x="280" y="30">
   </rect><text x="310" y="45">
   guard</text></g><path d="M340 41h20">
   </path></g></g><path d="M360 41h20">
   </path><path d="M40 41a10 10 0 0 1 10 10v50a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 111h32">
   </path><path d="M328 111h32">
   </path><path d="M92 111h10">
   </path><g class="terminal">
   <path d="M102 111h0">
   </path><path d="M146 111h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="102" y="100">
   </rect><text x="124" y="115">
   var</text></g><path d="M146 111h10">
   </path><path d="M156 111h10">
   </path><g class="non-terminal">
   <path d="M166 111h0">
   </path><path d="M218 111h0">
   </path><rect height="22" width="52" x="166" y="100">
   </rect><text x="192" y="115">
   noun</text></g><path d="M218 111h10">
   </path><g>
   <path d="M228 111h0">
   </path><path d="M328 111h0">
   </path><path d="M228 111a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M248 91h60">
   </path></g><path d="M308 91a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M228 111h20">
   </path><g class="non-terminal">
   <path d="M248 111h0">
   </path><path d="M308 111h0">
   </path><rect height="22" width="60" x="248" y="100">
   </rect><text x="278" y="115">
   guard</text></g><path d="M308 111h20">
   </path></g></g><path d="M360 111a10 10 0 0 0 10 -10v-50a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v90a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 151h40">
   </path><path d="M320 151h40">
   </path><path d="M100 151h10">
   </path><g class="terminal">
   <path d="M110 151h0">
   </path><path d="M138 151h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="110" y="140">
   </rect><text x="124" y="155">
   &amp;</text></g><path d="M138 151h10">
   </path><path d="M148 151h10">
   </path><g class="non-terminal">
   <path d="M158 151h0">
   </path><path d="M210 151h0">
   </path><rect height="22" width="52" x="158" y="140">
   </rect><text x="184" y="155">
   noun</text></g><path d="M210 151h10">
   </path><g>
   <path d="M220 151h0">
   </path><path d="M320 151h0">
   </path><path d="M220 151a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M240 131h60">
   </path></g><path d="M300 131a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M220 151h20">
   </path><g class="non-terminal">
   <path d="M240 151h0">
   </path><path d="M300 151h0">
   </path><rect height="22" width="60" x="240" y="140">
   </rect><text x="270" y="155">
   guard</text></g><path d="M300 151h20">
   </path></g></g><path d="M360 151a10 10 0 0 0 10 -10v-90a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v130a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 191h28">
   </path><path d="M332 191h28">
   </path><path d="M88 191h10">
   </path><g class="terminal">
   <path d="M98 191h0">
   </path><path d="M150 191h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="98" y="180">
   </rect><text x="124" y="195">
   bind</text></g><path d="M150 191h10">
   </path><path d="M160 191h10">
   </path><g class="non-terminal">
   <path d="M170 191h0">
   </path><path d="M222 191h0">
   </path><rect height="22" width="52" x="170" y="180">
   </rect><text x="196" y="195">
   noun</text></g><path d="M222 191h10">
   </path><g>
   <path d="M232 191h0">
   </path><path d="M332 191h0">
   </path><path d="M232 191a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M252 171h60">
   </path></g><path d="M312 171a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M232 191h20">
   </path><g class="non-terminal">
   <path d="M252 191h0">
   </path><path d="M312 191h0">
   </path><rect height="22" width="60" x="252" y="180">
   </rect><text x="282" y="195">
   guard</text></g><path d="M312 191h20">
   </path></g></g><path d="M360 191a10 10 0 0 0 10 -10v-130a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v160a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 221h86">
   </path><path d="M274 221h86">
   </path><path d="M146 221h10">
   </path><g class="terminal">
   <path d="M156 221h0">
   </path><path d="M192 221h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="156" y="210">
   </rect><text x="174" y="225">
   &amp;&amp;</text></g><path d="M192 221h10">
   </path><path d="M202 221h10">
   </path><g class="non-terminal">
   <path d="M212 221h0">
   </path><path d="M264 221h0">
   </path><rect height="22" width="52" x="212" y="210">
   </rect><text x="238" y="225">
   noun</text></g><path d="M264 221h10">
   </path></g><path d="M360 221a10 10 0 0 0 10 -10v-160a10 10 0 0 1 10 -10">
   </path></g><path d="M 380 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

noun
----

.. raw:: html

   <svg class="railroad-diagram" height="92" viewBox="0 0 281 92" width="281" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M240 31h0">
   </path><path d="M40 31h20">
   </path><g class="terminal">
   <path d="M60 31h30">
   </path><path d="M190 31h30">
   </path><rect height="22" rx="10" ry="10" width="100" x="90" y="20">
   </rect><text x="140" y="35">
   IDENTIFIER</text></g><path d="M220 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 61h0">
   </path><path d="M220 61h0">
   </path><path d="M60 61h10">
   </path><g class="terminal">
   <path d="M70 61h0">
   </path><path d="M106 61h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="70" y="50">
   </rect><text x="88" y="65">
   ::</text></g><path d="M106 61h10">
   </path><path d="M116 61h10">
   </path><g class="terminal">
   <path d="M126 61h0">
   </path><path d="M210 61h0">
   </path><rect height="22" rx="10" ry="10" width="84" x="126" y="50">
   </rect><text x="168" y="65">
   .String.</text></g><path d="M210 61h10">
   </path></g><path d="M220 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M 240 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

quasiliteral
------------

.. raw:: html

   <svg class="railroad-diagram" height="200" viewBox="0 0 657 200" width="657" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M616 41h0">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M180 41h0">
   </path><path d="M40 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M60 21h100">
   </path></g><path d="M160 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M40 41h20">
   </path><g class="terminal">
   <path d="M60 41h0">
   </path><path d="M160 41h0">
   </path><rect height="22" rx="10" ry="10" width="100" x="60" y="30">
   </rect><text x="110" y="45">
   IDENTIFIER</text></g><path d="M160 41h20">
   </path></g><path d="M180 41h10">
   </path><g class="terminal">
   <path d="M190 41h0">
   </path><path d="M218 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="190" y="30">
   </rect><text x="204" y="45">
   `</text></g><path d="M218 41h10">
   </path><g>
   <path d="M228 41h0">
   </path><path d="M568 41h0">
   </path><path d="M228 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M248 21h300">
   </path></g><path d="M548 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M228 41h20">
   </path><g>
   <path d="M248 41h0">
   </path><path d="M548 41h0">
   </path><path d="M248 41h10">
   </path><g>
   <path d="M258 41h0">
   </path><path d="M538 41h0">
   </path><path d="M258 41h20">
   </path><g>
   <path d="M278 41h80">
   </path><path d="M438 41h80">
   </path><text class="comment" x="398" y="46">
   ...text...</text></g><path d="M518 41h20">
   </path><path d="M258 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M278 71h12">
   </path><path d="M506 71h12">
   </path><path d="M290 71h20">
   </path><g class="terminal">
   <path d="M310 71h54">
   </path><path d="M432 71h54">
   </path><rect height="22" rx="10" ry="10" width="68" x="364" y="60">
   </rect><text x="398" y="75">
   $IDENT</text></g><path d="M486 71h20">
   </path><path d="M290 71a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M310 101h0">
   </path><path d="M486 101h0">
   </path><path d="M310 101h10">
   </path><g class="terminal">
   <path d="M320 101h0">
   </path><path d="M356 101h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="320" y="90">
   </rect><text x="338" y="105">
   ${</text></g><path d="M356 101h10">
   </path><path d="M366 101h10">
   </path><g class="non-terminal">
   <path d="M376 101h0">
   </path><path d="M428 101h0">
   </path><rect height="22" width="52" x="376" y="90">
   </rect><text x="402" y="105">
   expr</text></g><path d="M428 101h10">
   </path><path d="M438 101h10">
   </path><g class="terminal">
   <path d="M448 101h0">
   </path><path d="M476 101h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="448" y="90">
   </rect><text x="462" y="105">
   }</text></g><path d="M476 101h10">
   </path></g><path d="M486 101a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M518 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M258 41a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g>
   <path d="M278 131h0">
   </path><path d="M518 131h0">
   </path><path d="M278 131h20">
   </path><g class="terminal">
   <path d="M298 131h66">
   </path><path d="M432 131h66">
   </path><rect height="22" rx="10" ry="10" width="68" x="364" y="120">
   </rect><text x="398" y="135">
   @IDENT</text></g><path d="M498 131h20">
   </path><path d="M278 131a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M298 161h0">
   </path><path d="M498 161h0">
   </path><path d="M298 161h10">
   </path><g class="terminal">
   <path d="M308 161h0">
   </path><path d="M344 161h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="308" y="150">
   </rect><text x="326" y="165">
   @{</text></g><path d="M344 161h10">
   </path><path d="M354 161h10">
   </path><g class="non-terminal">
   <path d="M364 161h0">
   </path><path d="M440 161h0">
   </path><rect height="22" width="76" x="364" y="150">
   </rect><text x="402" y="165">
   pattern</text></g><path d="M440 161h10">
   </path><path d="M450 161h10">
   </path><g class="terminal">
   <path d="M460 161h0">
   </path><path d="M488 161h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="460" y="150">
   </rect><text x="474" y="165">
   }</text></g><path d="M488 161h10">
   </path></g><path d="M498 161a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M518 131a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path></g><path d="M538 41h10">
   </path><path d="M258 41a10 10 0 0 0 -10 10v119a10 10 0 0 0 10 10">
   </path><g>
   <path d="M258 180h280">
   </path></g><path d="M538 180a10 10 0 0 0 10 -10v-119a10 10 0 0 0 -10 -10">
   </path></g><path d="M548 41h20">
   </path></g><path d="M568 41h10">
   </path><g class="terminal">
   <path d="M578 41h0">
   </path><path d="M606 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="578" y="30">
   </rect><text x="592" y="45">
   `</text></g><path d="M606 41h10">
   </path></g><path d="M 616 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

mapPatternItem
--------------

.. raw:: html

   <svg class="railroad-diagram" height="222" viewBox="0 0 657 222" width="657" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M616 41h0">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M440 41h0">
   </path><path d="M40 41h20">
   </path><g>
   <path d="M60 41h88">
   </path><path d="M332 41h88">
   </path><path d="M148 41h10">
   </path><g class="terminal">
   <path d="M158 41h0">
   </path><path d="M194 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="158" y="30">
   </rect><text x="176" y="45">
   =></text></g><path d="M194 41h10">
   </path><path d="M204 41h10">
   </path><g class="non-terminal">
   <path d="M214 41h0">
   </path><path d="M322 41h0">
   </path><rect height="22" width="108" x="214" y="30">
   </rect><text x="268" y="45">
   namePattern</text></g><path d="M322 41h10">
   </path></g><path d="M420 41h20">
   </path><path d="M40 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 71h0">
   </path><path d="M420 71h0">
   </path><g>
   <path d="M60 71h0">
   </path><path d="M268 71h0">
   </path><path d="M60 71h20">
   </path><g>
   <path d="M80 71h0">
   </path><path d="M248 71h0">
   </path><path d="M80 71h10">
   </path><g class="terminal">
   <path d="M90 71h0">
   </path><path d="M118 71h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="90" y="60">
   </rect><text x="104" y="75">
   (</text></g><path d="M118 71h10">
   </path><path d="M128 71h10">
   </path><g class="non-terminal">
   <path d="M138 71h0">
   </path><path d="M190 71h0">
   </path><rect height="22" width="52" x="138" y="60">
   </rect><text x="164" y="75">
   expr</text></g><path d="M190 71h10">
   </path><path d="M200 71h10">
   </path><g class="terminal">
   <path d="M210 71h0">
   </path><path d="M238 71h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="210" y="60">
   </rect><text x="224" y="75">
   )</text></g><path d="M238 71h10">
   </path></g><path d="M248 71h20">
   </path><path d="M60 71a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M80 101h42">
   </path><path d="M206 101h42">
   </path><rect height="22" rx="10" ry="10" width="84" x="122" y="90">
   </rect><text x="164" y="105">
   .String.</text></g><path d="M248 101a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M60 71a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M80 131h54">
   </path><path d="M194 131h54">
   </path><rect height="22" rx="10" ry="10" width="60" x="134" y="120">
   </rect><text x="164" y="135">
   .int.</text></g><path d="M248 131a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path><path d="M60 71a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M80 161h38">
   </path><path d="M210 161h38">
   </path><rect height="22" rx="10" ry="10" width="92" x="118" y="150">
   </rect><text x="164" y="165">
   .float64.</text></g><path d="M248 161a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path><path d="M60 71a10 10 0 0 1 10 10v100a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M80 191h50">
   </path><path d="M198 191h50">
   </path><rect height="22" rx="10" ry="10" width="68" x="130" y="180">
   </rect><text x="164" y="195">
   .char.</text></g><path d="M248 191a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path></g><path d="M268 71h10">
   </path><g class="terminal">
   <path d="M278 71h0">
   </path><path d="M314 71h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="278" y="60">
   </rect><text x="296" y="75">
   =></text></g><path d="M314 71h10">
   </path><path d="M324 71h10">
   </path><g class="non-terminal">
   <path d="M334 71h0">
   </path><path d="M410 71h0">
   </path><rect height="22" width="76" x="334" y="60">
   </rect><text x="372" y="75">
   pattern</text></g><path d="M410 71h10">
   </path></g><path d="M420 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M440 41h0">
   </path><path d="M616 41h0">
   </path><path d="M440 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M460 21h136">
   </path></g><path d="M596 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M440 41h20">
   </path><g>
   <path d="M460 41h0">
   </path><path d="M596 41h0">
   </path><path d="M460 41h10">
   </path><g class="terminal">
   <path d="M470 41h0">
   </path><path d="M506 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="470" y="30">
   </rect><text x="488" y="45">
   :=</text></g><path d="M506 41h10">
   </path><path d="M516 41h10">
   </path><g class="non-terminal">
   <path d="M526 41h0">
   </path><path d="M586 41h0">
   </path><rect height="22" width="60" x="526" y="30">
   </rect><text x="556" y="45">
   order</text></g><path d="M586 41h10">
   </path></g><path d="M596 41h20">
   </path></g></g><path d="M 616 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

mapItem
-------

.. raw:: html

   <svg class="railroad-diagram" height="152" viewBox="0 0 345 152" width="345" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M304 31h0">
   </path><path d="M40 31h20">
   </path><g>
   <path d="M60 31h0">
   </path><path d="M284 31h0">
   </path><path d="M60 31h10">
   </path><g class="terminal">
   <path d="M70 31h0">
   </path><path d="M106 31h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="70" y="20">
   </rect><text x="88" y="35">
   =></text></g><path d="M106 31h10">
   </path><g>
   <path d="M116 31h0">
   </path><path d="M284 31h0">
   </path><path d="M116 31h20">
   </path><g>
   <path d="M136 31h4">
   </path><path d="M260 31h4">
   </path><path d="M140 31h10">
   </path><g class="terminal">
   <path d="M150 31h0">
   </path><path d="M178 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="150" y="20">
   </rect><text x="164" y="35">
   &amp;</text></g><path d="M178 31h10">
   </path><path d="M188 31h10">
   </path><g class="non-terminal">
   <path d="M198 31h0">
   </path><path d="M250 31h0">
   </path><rect height="22" width="52" x="198" y="20">
   </rect><text x="224" y="35">
   noun</text></g><path d="M250 31h10">
   </path></g><path d="M264 31h20">
   </path><path d="M116 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M136 61h0">
   </path><path d="M264 61h0">
   </path><path d="M136 61h10">
   </path><g class="terminal">
   <path d="M146 61h0">
   </path><path d="M182 61h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="146" y="50">
   </rect><text x="164" y="65">
   &amp;&amp;</text></g><path d="M182 61h10">
   </path><path d="M192 61h10">
   </path><g class="non-terminal">
   <path d="M202 61h0">
   </path><path d="M254 61h0">
   </path><rect height="22" width="52" x="202" y="50">
   </rect><text x="228" y="65">
   noun</text></g><path d="M254 61h10">
   </path></g><path d="M264 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M116 31a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M136 91h38">
   </path><path d="M226 91h38">
   </path><rect height="22" width="52" x="174" y="80">
   </rect><text x="200" y="95">
   noun</text></g><path d="M264 91a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path></g></g><path d="M284 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 121h12">
   </path><path d="M272 121h12">
   </path><path d="M72 121h10">
   </path><g class="non-terminal">
   <path d="M82 121h0">
   </path><path d="M134 121h0">
   </path><rect height="22" width="52" x="82" y="110">
   </rect><text x="108" y="125">
   expr</text></g><path d="M134 121h10">
   </path><path d="M144 121h10">
   </path><g class="terminal">
   <path d="M154 121h0">
   </path><path d="M190 121h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="154" y="110">
   </rect><text x="172" y="125">
   =></text></g><path d="M190 121h10">
   </path><path d="M200 121h10">
   </path><g class="non-terminal">
   <path d="M210 121h0">
   </path><path d="M262 121h0">
   </path><rect height="22" width="52" x="210" y="110">
   </rect><text x="236" y="125">
   expr</text></g><path d="M262 121h10">
   </path></g><path d="M284 121a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path></g><path d="M 304 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>
