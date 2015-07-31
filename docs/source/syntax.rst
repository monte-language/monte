
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

.. index::
   single: syntax; module

**module**

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

.. index::
   single: syntax; imports

**imports**

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

.. index::
   single: syntax; exports

**exports**

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

.. index::
   single: syntax; block

**block**

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

.. index::
   single: syntax; blockExpr

**blockExpr**

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

.. index::
   single: syntax; if

**if**

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

.. index::
   single: syntax; escape

**escape**

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

.. index::
   single: syntax; blockCatch

**blockCatch**

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

.. index::
   single: syntax; for

**for**

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

.. index::
   single: syntax; fn

**fn**

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

.. index::
   single: syntax; switch

**switch**

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

.. index::
   single: syntax; try

**try**

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

.. index::
   single: syntax; catchers

**catchers**

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

.. index::
   single: syntax; while

**while**

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

.. index::
   single: syntax; when

**when**

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

.. index::
   single: syntax; bind

**bind**

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

.. index::
   single: syntax; object

**object**

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

.. index::
   single: syntax; objectExpr

**objectExpr**

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

.. index::
   single: syntax; objectScript

**objectScript**

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

.. index::
   single: syntax; doco

**doco**

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

.. index::
   single: syntax; def

**def**

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

.. index::
   single: syntax; interface

**interface**

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

.. index::
   single: syntax; meta

**meta**

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

.. index::
   single: syntax; guard

**guard**

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
