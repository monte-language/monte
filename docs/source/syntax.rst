
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
        /*font-style: italic;*/
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

   <svg class="railroad-diagram" height="132" viewBox="0 0 369 132" width="369" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M328 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M78 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="50" y="30">
   </rect><text x="64" y="45">
   {</text></g><path d="M78 41h10">
   </path><g>
   <path d="M88 41h0">
   </path><path d="M280 41h0">
   </path><path d="M88 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M108 21h152">
   </path></g><path d="M260 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M88 41h20">
   </path><g>
   <path d="M108 41h0">
   </path><path d="M260 41h0">
   </path><path d="M108 41h10">
   </path><g>
   <path d="M118 41h0">
   </path><path d="M250 41h0">
   </path><path d="M118 41h20">
   </path><g class="non-terminal">
   <path d="M138 41h0">
   </path><path d="M230 41h0">
   </path><rect height="22" width="92" x="138" y="30">
   </rect><text x="184" y="45">
   blockExpr</text></g><path d="M230 41h20">
   </path><path d="M118 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M138 71h20">
   </path><path d="M210 71h20">
   </path><rect height="22" width="52" x="158" y="60">
   </rect><text x="184" y="75">
   expr</text></g><path d="M230 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M250 41h10">
   </path><path d="M118 41a10 10 0 0 0 -10 10v40a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M118 101h52">
   </path><path d="M198 101h52">
   </path><rect height="22" rx="10" ry="10" width="28" x="170" y="90">
   </rect><text x="184" y="105">
   ;</text></g><path d="M250 101a10 10 0 0 0 10 -10v-40a10 10 0 0 0 -10 -10">
   </path></g><path d="M260 41h20">
   </path></g><path d="M280 41h10">
   </path><g class="terminal">
   <path d="M290 41h0">
   </path><path d="M318 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="290" y="30">
   </rect><text x="304" y="45">
   }</text></g><path d="M318 41h10">
   </path></g><path d="M 328 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

blockExpr
---------

.. raw:: html

   <svg class="railroad-diagram" height="452" viewBox="0 0 213 452" width="213" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
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
   </path><path d="M40 31a10 10 0 0 1 10 10v370a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 421h20">
   </path><path d="M132 421h20">
   </path><rect height="22" width="52" x="80" y="410">
   </rect><text x="106" y="425">
   pass</text></g><path d="M152 421a10 10 0 0 0 10 -10v-370a10 10 0 0 1 10 -10">
   </path></g><path d="M 172 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

if
--

.. raw:: html

   <svg class="railroad-diagram" height="102" viewBox="0 0 721 102" width="721" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M680 41h0">
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
   </path><path d="M680 41h0">
   </path><path d="M344 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M364 21h296">
   </path></g><path d="M660 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M344 41h20">
   </path><g>
   <path d="M364 41h0">
   </path><path d="M660 41h0">
   </path><path d="M364 41h10">
   </path><g class="terminal">
   <path d="M374 41h0">
   </path><path d="M426 41h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="374" y="30">
   </rect><text x="400" y="45">
   else</text></g><path d="M426 41h10">
   </path><g>
   <path d="M436 41h0">
   </path><path d="M660 41h0">
   </path><path d="M436 41h20">
   </path><g>
   <path d="M456 41h0">
   </path><path d="M640 41h0">
   </path><path d="M456 41h10">
   </path><g class="terminal">
   <path d="M466 41h0">
   </path><path d="M502 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="466" y="30">
   </rect><text x="484" y="45">
   if</text></g><path d="M502 41h10">
   </path><path d="M512 41h10">
   </path><g class="non-terminal">
   <path d="M522 41h0">
   </path><path d="M630 41h0">
   </path><rect height="22" width="108" x="522" y="30">
   </rect><text x="576" y="45">
   blockExpr@@</text></g><path d="M630 41h10">
   </path></g><path d="M640 41h20">
   </path><path d="M436 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M456 71h62">
   </path><path d="M578 71h62">
   </path><rect height="22" width="60" x="518" y="60">
   </rect><text x="548" y="75">
   block</text></g><path d="M640 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g></g><path d="M660 41h20">
   </path></g></g><path d="M 680 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

escape
------

.. raw:: html

   <svg class="railroad-diagram" height="72" viewBox="0 0 641 72" width="641" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M600 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M118 41h0">
   </path><rect height="22" rx="10" ry="10" width="68" x="50" y="30">
   </rect><text x="84" y="45">
   escape</text></g><path d="M118 41h10">
   </path><path d="M128 41h10">
   </path><g class="non-terminal">
   <path d="M138 41h0">
   </path><path d="M214 41h0">
   </path><rect height="22" width="76" x="138" y="30">
   </rect><text x="176" y="45">
   pattern</text></g><path d="M214 41h10">
   </path><path d="M224 41h10">
   </path><g class="non-terminal">
   <path d="M234 41h0">
   </path><path d="M294 41h0">
   </path><rect height="22" width="60" x="234" y="30">
   </rect><text x="264" y="45">
   block</text></g><path d="M294 41h10">
   </path><g>
   <path d="M304 41h0">
   </path><path d="M600 41h0">
   </path><path d="M304 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M324 21h256">
   </path></g><path d="M580 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M304 41h20">
   </path><g>
   <path d="M324 41h0">
   </path><path d="M580 41h0">
   </path><path d="M324 41h10">
   </path><g class="terminal">
   <path d="M334 41h0">
   </path><path d="M394 41h0">
   </path><rect height="22" rx="10" ry="10" width="60" x="334" y="30">
   </rect><text x="364" y="45">
   catch</text></g><path d="M394 41h10">
   </path><path d="M404 41h10">
   </path><g class="non-terminal">
   <path d="M414 41h0">
   </path><path d="M490 41h0">
   </path><rect height="22" width="76" x="414" y="30">
   </rect><text x="452" y="45">
   pattern</text></g><path d="M490 41h10">
   </path><path d="M500 41h10">
   </path><g class="non-terminal">
   <path d="M510 41h0">
   </path><path d="M570 41h0">
   </path><rect height="22" width="60" x="510" y="30">
   </rect><text x="540" y="45">
   block</text></g><path d="M570 41h10">
   </path></g><path d="M580 41h20">
   </path></g></g><path d="M 600 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

for
---

.. raw:: html

   <svg class="railroad-diagram" height="72" viewBox="0 0 937 72" width="937" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M896 41h0">
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
   </path><path d="M590 41h0">
   </path><rect height="22" width="60" x="530" y="30">
   </rect><text x="560" y="45">
   block</text></g><path d="M590 41h10">
   </path><g>
   <path d="M600 41h0">
   </path><path d="M896 41h0">
   </path><path d="M600 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M620 21h256">
   </path></g><path d="M876 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M600 41h20">
   </path><g>
   <path d="M620 41h0">
   </path><path d="M876 41h0">
   </path><path d="M620 41h10">
   </path><g class="terminal">
   <path d="M630 41h0">
   </path><path d="M690 41h0">
   </path><rect height="22" rx="10" ry="10" width="60" x="630" y="30">
   </rect><text x="660" y="45">
   catch</text></g><path d="M690 41h10">
   </path><path d="M700 41h10">
   </path><g class="non-terminal">
   <path d="M710 41h0">
   </path><path d="M786 41h0">
   </path><rect height="22" width="76" x="710" y="30">
   </rect><text x="748" y="45">
   pattern</text></g><path d="M786 41h10">
   </path><path d="M796 41h10">
   </path><g class="non-terminal">
   <path d="M806 41h0">
   </path><path d="M866 41h0">
   </path><rect height="22" width="60" x="806" y="30">
   </rect><text x="836" y="45">
   block</text></g><path d="M866 41h10">
   </path></g><path d="M876 41h20">
   </path></g></g><path d="M 896 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
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

   <svg class="railroad-diagram" height="81" viewBox="0 0 757 81" width="757" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M716 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M94 41h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="50" y="30">
   </rect><text x="72" y="45">
   try</text></g><path d="M94 41h10">
   </path><path d="M104 41h10">
   </path><g class="non-terminal">
   <path d="M114 41h0">
   </path><path d="M174 41h0">
   </path><rect height="22" width="60" x="114" y="30">
   </rect><text x="144" y="45">
   block</text></g><path d="M174 41h10">
   </path><g>
   <path d="M184 41h0">
   </path><path d="M500 41h0">
   </path><path d="M184 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M204 21h276">
   </path></g><path d="M480 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M184 41h20">
   </path><g>
   <path d="M204 41h0">
   </path><path d="M480 41h0">
   </path><path d="M204 41h10">
   </path><g>
   <path d="M214 41h0">
   </path><path d="M470 41h0">
   </path><path d="M214 41h10">
   </path><g class="terminal">
   <path d="M224 41h0">
   </path><path d="M284 41h0">
   </path><rect height="22" rx="10" ry="10" width="60" x="224" y="30">
   </rect><text x="254" y="45">
   catch</text></g><path d="M284 41h10">
   </path><path d="M294 41h10">
   </path><g class="non-terminal">
   <path d="M304 41h0">
   </path><path d="M380 41h0">
   </path><rect height="22" width="76" x="304" y="30">
   </rect><text x="342" y="45">
   pattern</text></g><path d="M380 41h10">
   </path><path d="M390 41h10">
   </path><g class="non-terminal">
   <path d="M400 41h0">
   </path><path d="M460 41h0">
   </path><rect height="22" width="60" x="400" y="30">
   </rect><text x="430" y="45">
   block</text></g><path d="M460 41h10">
   </path></g><path d="M470 41h10">
   </path><path d="M214 41a10 10 0 0 0 -10 10v0a10 10 0 0 0 10 10">
   </path><g>
   <path d="M214 61h256">
   </path></g><path d="M470 61a10 10 0 0 0 10 -10v0a10 10 0 0 0 -10 -10">
   </path></g><path d="M480 41h20">
   </path></g><g>
   <path d="M500 41h0">
   </path><path d="M716 41h0">
   </path><path d="M500 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M520 21h176">
   </path></g><path d="M696 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M500 41h20">
   </path><g>
   <path d="M520 41h0">
   </path><path d="M696 41h0">
   </path><path d="M520 41h10">
   </path><g class="terminal">
   <path d="M530 41h0">
   </path><path d="M606 41h0">
   </path><rect height="22" rx="10" ry="10" width="76" x="530" y="30">
   </rect><text x="568" y="45">
   finally</text></g><path d="M606 41h10">
   </path><path d="M616 41h10">
   </path><g class="non-terminal">
   <path d="M626 41h0">
   </path><path d="M686 41h0">
   </path><rect height="22" width="60" x="626" y="30">
   </rect><text x="656" y="45">
   block</text></g><path d="M686 41h10">
   </path></g><path d="M696 41h20">
   </path></g></g><path d="M 716 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

while
-----

.. raw:: html

   <svg class="railroad-diagram" height="72" viewBox="0 0 705 72" width="705" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M664 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M110 41h0">
   </path><rect height="22" rx="10" ry="10" width="60" x="50" y="30">
   </rect><text x="80" y="45">
   while</text></g><path d="M110 41h10">
   </path><path d="M120 41h10">
   </path><g class="terminal">
   <path d="M130 41h0">
   </path><path d="M158 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="130" y="30">
   </rect><text x="144" y="45">
   (</text></g><path d="M158 41h10">
   </path><path d="M168 41h10">
   </path><g class="non-terminal">
   <path d="M178 41h0">
   </path><path d="M230 41h0">
   </path><rect height="22" width="52" x="178" y="30">
   </rect><text x="204" y="45">
   expr</text></g><path d="M230 41h10">
   </path><path d="M240 41h10">
   </path><g class="terminal">
   <path d="M250 41h0">
   </path><path d="M278 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="250" y="30">
   </rect><text x="264" y="45">
   )</text></g><path d="M278 41h10">
   </path><path d="M288 41h10">
   </path><g class="non-terminal">
   <path d="M298 41h0">
   </path><path d="M358 41h0">
   </path><rect height="22" width="60" x="298" y="30">
   </rect><text x="328" y="45">
   block</text></g><path d="M358 41h10">
   </path><g>
   <path d="M368 41h0">
   </path><path d="M664 41h0">
   </path><path d="M368 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M388 21h256">
   </path></g><path d="M644 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M368 41h20">
   </path><g>
   <path d="M388 41h0">
   </path><path d="M644 41h0">
   </path><path d="M388 41h10">
   </path><g class="terminal">
   <path d="M398 41h0">
   </path><path d="M458 41h0">
   </path><rect height="22" rx="10" ry="10" width="60" x="398" y="30">
   </rect><text x="428" y="45">
   catch</text></g><path d="M458 41h10">
   </path><path d="M468 41h10">
   </path><g class="non-terminal">
   <path d="M478 41h0">
   </path><path d="M554 41h0">
   </path><rect height="22" width="76" x="478" y="30">
   </rect><text x="516" y="45">
   pattern</text></g><path d="M554 41h10">
   </path><path d="M564 41h10">
   </path><g class="non-terminal">
   <path d="M574 41h0">
   </path><path d="M634 41h0">
   </path><rect height="22" width="60" x="574" y="30">
   </rect><text x="604" y="45">
   block</text></g><path d="M634 41h10">
   </path></g><path d="M644 41h20">
   </path></g></g><path d="M 664 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

when
----

.. raw:: html

   <svg class="railroad-diagram" height="102" viewBox="0 0 873 102" width="873" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M832 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M102 41h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="50" y="30">
   </rect><text x="76" y="45">
   when</text></g><path d="M102 41h10">
   </path><path d="M112 41h10">
   </path><g class="terminal">
   <path d="M122 41h0">
   </path><path d="M150 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="122" y="30">
   </rect><text x="136" y="45">
   (</text></g><path d="M150 41h10">
   </path><path d="M160 41h10">
   </path><g>
   <path d="M170 41h0">
   </path><path d="M242 41h0">
   </path><path d="M170 41h10">
   </path><g class="non-terminal">
   <path d="M180 41h0">
   </path><path d="M232 41h0">
   </path><rect height="22" width="52" x="180" y="30">
   </rect><text x="206" y="45">
   expr</text></g><path d="M232 41h10">
   </path><path d="M180 41a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M180 71h12">
   </path><path d="M220 71h12">
   </path><rect height="22" rx="10" ry="10" width="28" x="192" y="60">
   </rect><text x="206" y="75">
   ,</text></g><path d="M232 71a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M242 41h10">
   </path><path d="M252 41h10">
   </path><g class="terminal">
   <path d="M262 41h0">
   </path><path d="M290 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="262" y="30">
   </rect><text x="276" y="45">
   )</text></g><path d="M290 41h10">
   </path><g>
   <path d="M300 41h0">
   </path><path d="M616 41h0">
   </path><path d="M300 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M320 21h276">
   </path></g><path d="M596 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M300 41h20">
   </path><g>
   <path d="M320 41h0">
   </path><path d="M596 41h0">
   </path><path d="M320 41h10">
   </path><g>
   <path d="M330 41h0">
   </path><path d="M586 41h0">
   </path><path d="M330 41h10">
   </path><g class="terminal">
   <path d="M340 41h0">
   </path><path d="M400 41h0">
   </path><rect height="22" rx="10" ry="10" width="60" x="340" y="30">
   </rect><text x="370" y="45">
   catch</text></g><path d="M400 41h10">
   </path><path d="M410 41h10">
   </path><g class="non-terminal">
   <path d="M420 41h0">
   </path><path d="M496 41h0">
   </path><rect height="22" width="76" x="420" y="30">
   </rect><text x="458" y="45">
   pattern</text></g><path d="M496 41h10">
   </path><path d="M506 41h10">
   </path><g class="non-terminal">
   <path d="M516 41h0">
   </path><path d="M576 41h0">
   </path><rect height="22" width="60" x="516" y="30">
   </rect><text x="546" y="45">
   block</text></g><path d="M576 41h10">
   </path></g><path d="M586 41h10">
   </path><path d="M330 41a10 10 0 0 0 -10 10v0a10 10 0 0 0 10 10">
   </path><g>
   <path d="M330 61h256">
   </path></g><path d="M586 61a10 10 0 0 0 10 -10v0a10 10 0 0 0 -10 -10">
   </path></g><path d="M596 41h20">
   </path></g><g>
   <path d="M616 41h0">
   </path><path d="M832 41h0">
   </path><path d="M616 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M636 21h176">
   </path></g><path d="M812 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M616 41h20">
   </path><g>
   <path d="M636 41h0">
   </path><path d="M812 41h0">
   </path><path d="M636 41h10">
   </path><g class="terminal">
   <path d="M646 41h0">
   </path><path d="M722 41h0">
   </path><rect height="22" rx="10" ry="10" width="76" x="646" y="30">
   </rect><text x="684" y="45">
   finally</text></g><path d="M722 41h10">
   </path><path d="M732 41h10">
   </path><g class="non-terminal">
   <path d="M742 41h0">
   </path><path d="M802 41h0">
   </path><rect height="22" width="60" x="742" y="30">
   </rect><text x="772" y="45">
   block</text></g><path d="M802 41h10">
   </path></g><path d="M812 41h20">
   </path></g></g><path d="M 832 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

bind
----

.. raw:: html

   <svg class="railroad-diagram" height="72" viewBox="0 0 529 72" width="529" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M488 41h0">
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
   </path><path d="M352 41h0">
   </path><path d="M184 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M204 21h128">
   </path></g><path d="M332 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M184 41h20">
   </path><g>
   <path d="M204 41h0">
   </path><path d="M332 41h0">
   </path><path d="M204 41h10">
   </path><g class="terminal">
   <path d="M214 41h0">
   </path><path d="M242 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="214" y="30">
   </rect><text x="228" y="45">
   :</text></g><path d="M242 41h10">
   </path><path d="M252 41h10">
   </path><g class="non-terminal">
   <path d="M262 41h0">
   </path><path d="M322 41h0">
   </path><rect height="22" width="60" x="262" y="30">
   </rect><text x="292" y="45">
   guard</text></g><path d="M322 41h10">
   </path></g><path d="M332 41h20">
   </path></g><path d="M352 41h10">
   </path><g class="terminal">
   <path d="M362 41h0">
   </path><path d="M478 41h0">
   </path><rect height="22" rx="10" ry="10" width="116" x="362" y="30">
   </rect><text x="420" y="45">
   objectExpr@@</text></g><path d="M478 41h10">
   </path></g><path d="M 488 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

object
------

.. raw:: html

   <svg class="railroad-diagram" height="132" viewBox="0 0 657 132" width="657" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M616 41h0">
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
   </path><path d="M480 41h0">
   </path><path d="M312 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M332 21h128">
   </path></g><path d="M460 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M312 41h20">
   </path><g>
   <path d="M332 41h0">
   </path><path d="M460 41h0">
   </path><path d="M332 41h10">
   </path><g class="terminal">
   <path d="M342 41h0">
   </path><path d="M370 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="342" y="30">
   </rect><text x="356" y="45">
   :</text></g><path d="M370 41h10">
   </path><path d="M380 41h10">
   </path><g class="non-terminal">
   <path d="M390 41h0">
   </path><path d="M450 41h0">
   </path><rect height="22" width="60" x="390" y="30">
   </rect><text x="420" y="45">
   guard</text></g><path d="M450 41h10">
   </path></g><path d="M460 41h20">
   </path></g><path d="M480 41h10">
   </path><g class="terminal">
   <path d="M490 41h0">
   </path><path d="M606 41h0">
   </path><rect height="22" rx="10" ry="10" width="116" x="490" y="30">
   </rect><text x="548" y="45">
   objectExpr@@</text></g><path d="M606 41h10">
   </path></g><path d="M 616 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

def
---

.. raw:: html

   <svg class="railroad-diagram" height="132" viewBox="0 0 725 132" width="725" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M684 41h0">
   </path><path d="M40 41h10">
   </path><g class="terminal">
   <path d="M50 41h0">
   </path><path d="M94 41h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="50" y="30">
   </rect><text x="72" y="45">
   def</text></g><path d="M94 41h10">
   </path><g>
   <path d="M104 41h0">
   </path><path d="M684 41h0">
   </path><path d="M104 41h20">
   </path><g>
   <path d="M124 41h0">
   </path><path d="M664 41h0">
   </path><g>
   <path d="M124 41h0">
   </path><path d="M476 41h0">
   </path><path d="M124 41h20">
   </path><g>
   <path d="M144 41h0">
   </path><path d="M456 41h0">
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
   </path><path d="M456 41h0">
   </path><path d="M288 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M308 21h128">
   </path></g><path d="M436 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M288 41h20">
   </path><g>
   <path d="M308 41h0">
   </path><path d="M436 41h0">
   </path><path d="M308 41h10">
   </path><g class="terminal">
   <path d="M318 41h0">
   </path><path d="M346 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="318" y="30">
   </rect><text x="332" y="45">
   :</text></g><path d="M346 41h10">
   </path><path d="M356 41h10">
   </path><g class="non-terminal">
   <path d="M366 41h0">
   </path><path d="M426 41h0">
   </path><rect height="22" width="60" x="366" y="30">
   </rect><text x="396" y="45">
   guard</text></g><path d="M426 41h10">
   </path></g><path d="M436 41h20">
   </path></g></g><path d="M456 41h20">
   </path><path d="M124 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M144 71h130">
   </path><path d="M326 71h130">
   </path><rect height="22" width="52" x="274" y="60">
   </rect><text x="300" y="75">
   noun</text></g><path d="M456 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M476 41h0">
   </path><path d="M664 41h0">
   </path><path d="M476 41h20">
   </path><g class="terminal">
   <path d="M496 41h0">
   </path><path d="M644 41h0">
   </path><rect height="22" rx="10" ry="10" width="148" x="496" y="30">
   </rect><text x="570" y="45">
   objectFunction@@</text></g><path d="M644 41h20">
   </path><path d="M476 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M496 71h40">
   </path><path d="M604 71h40">
   </path><rect height="22" width="68" x="536" y="60">
   </rect><text x="570" y="75">
   assign</text></g><path d="M644 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g></g><path d="M664 41h20">
   </path><path d="M104 41a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M124 101h236">
   </path><path d="M428 101h236">
   </path><rect height="22" width="68" x="360" y="90">
   </rect><text x="394" y="105">
   assign</text></g><path d="M664 101a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path></g></g><path d="M 684 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

interface
---------

.. raw:: html

   <svg class="railroad-diagram" height="102" viewBox="0 0 1013 102" width="1013" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M972 41h0">
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
   </path><g class="terminal">
   <path d="M750 41h0">
   </path><path d="M874 41h0">
   </path><rect height="22" rx="10" ry="10" width="124" x="750" y="30">
   </rect><text x="812" y="45">
   implements_@@</text></g><path d="M874 41h10">
   </path><path d="M884 41h10">
   </path><g class="terminal">
   <path d="M894 41h0">
   </path><path d="M962 41h0">
   </path><rect height="22" rx="10" ry="10" width="68" x="894" y="30">
   </rect><text x="928" y="45">
   msgs@@</text></g><path d="M962 41h10">
   </path></g><path d="M 972 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
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

pass
----

.. raw:: html

   <svg class="railroad-diagram" height="62" viewBox="0 0 153 62" width="153" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><path d="M40 31h10">
   </path><g class="terminal">
   <path d="M50 31h0">
   </path><path d="M102 31h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="50" y="20">
   </rect><text x="76" y="35">
   pass</text></g><path d="M102 31h10">
   </path><path d="M 112 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

guard
-----

.. raw:: html

   <svg class="railroad-diagram" height="132" viewBox="0 0 469 132" width="469" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M428 41h0">
   </path><path d="M40 41h20">
   </path><g>
   <path d="M60 41h0">
   </path><path d="M408 41h0">
   </path><path d="M60 41h10">
   </path><g class="terminal">
   <path d="M70 41h0">
   </path><path d="M170 41h0">
   </path><rect height="22" rx="10" ry="10" width="100" x="70" y="30">
   </rect><text x="120" y="45">
   IDENTIFIER</text></g><path d="M170 41h10">
   </path><g>
   <path d="M180 41h0">
   </path><path d="M408 41h0">
   </path><path d="M180 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M200 21h188">
   </path></g><path d="M388 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M180 41h20">
   </path><g>
   <path d="M200 41h0">
   </path><path d="M388 41h0">
   </path><path d="M200 41h10">
   </path><g class="terminal">
   <path d="M210 41h0">
   </path><path d="M238 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="210" y="30">
   </rect><text x="224" y="45">
   [</text></g><path d="M238 41h10">
   </path><path d="M248 41h10">
   </path><g>
   <path d="M258 41h0">
   </path><path d="M330 41h0">
   </path><path d="M258 41h10">
   </path><g class="non-terminal">
   <path d="M268 41h0">
   </path><path d="M320 41h0">
   </path><rect height="22" width="52" x="268" y="30">
   </rect><text x="294" y="45">
   expr</text></g><path d="M320 41h10">
   </path><path d="M268 41a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M268 71h12">
   </path><path d="M308 71h12">
   </path><rect height="22" rx="10" ry="10" width="28" x="280" y="60">
   </rect><text x="294" y="75">
   ,</text></g><path d="M320 71a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M330 41h10">
   </path><path d="M340 41h10">
   </path><g class="terminal">
   <path d="M350 41h0">
   </path><path d="M378 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="350" y="30">
   </rect><text x="364" y="45">
   ]</text></g><path d="M378 41h10">
   </path></g><path d="M388 41h20">
   </path></g></g><path d="M408 41h20">
   </path><path d="M40 41a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 101h90">
   </path><path d="M318 101h90">
   </path><path d="M150 101h10">
   </path><g class="terminal">
   <path d="M160 101h0">
   </path><path d="M188 101h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="160" y="90">
   </rect><text x="174" y="105">
   (</text></g><path d="M188 101h10">
   </path><path d="M198 101h10">
   </path><g class="non-terminal">
   <path d="M208 101h0">
   </path><path d="M260 101h0">
   </path><rect height="22" width="52" x="208" y="90">
   </rect><text x="234" y="105">
   expr</text></g><path d="M260 101h10">
   </path><path d="M270 101h10">
   </path><g class="terminal">
   <path d="M280 101h0">
   </path><path d="M308 101h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="280" y="90">
   </rect><text x="294" y="105">
   )</text></g><path d="M308 101h10">
   </path></g><path d="M408 101a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path></g><path d="M 428 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
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
   </path><g class="terminal">
   <path d="M60 161h218">
   </path><path d="M378 161h218">
   </path><rect height="22" rx="10" ry="10" width="100" x="278" y="150">
   </rect><text x="328" y="165">
   @op=...XXX</text></g><path d="M596 161a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v130a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M60 191h198">
   </path><path d="M398 191h198">
   </path><rect height="22" rx="10" ry="10" width="140" x="258" y="180">
   </rect><text x="328" y="195">
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

   <svg class="railroad-diagram" height="222" viewBox="0 0 361 222" width="361" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 21 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 31h0">
   </path><path d="M320 31h0">
   </path><path d="M40 31h20">
   </path><g>
   <path d="M60 31h60">
   </path><path d="M240 31h60">
   </path><path d="M120 31h10">
   </path><g class="terminal">
   <path d="M130 31h0">
   </path><path d="M158 31h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="130" y="20">
   </rect><text x="144" y="35">
   -</text></g><path d="M158 31h10">
   </path><path d="M168 31h10">
   </path><g class="non-terminal">
   <path d="M178 31h0">
   </path><path d="M230 31h0">
   </path><rect height="22" width="52" x="178" y="20">
   </rect><text x="204" y="35">
   prim</text></g><path d="M230 31h10">
   </path></g><path d="M300 31h20">
   </path><path d="M40 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 61h50">
   </path><path d="M250 61h50">
   </path><g>
   <path d="M110 61h0">
   </path><path d="M178 61h0">
   </path><path d="M110 61h20">
   </path><g class="terminal">
   <path d="M130 61h0">
   </path><path d="M158 61h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="130" y="50">
   </rect><text x="144" y="65">
   ~</text></g><path d="M158 61h20">
   </path><path d="M110 61a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M130 91h0">
   </path><path d="M158 91h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="130" y="80">
   </rect><text x="144" y="95">
   !</text></g><path d="M158 91a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M178 61h10">
   </path><g class="non-terminal">
   <path d="M188 61h0">
   </path><path d="M240 61h0">
   </path><rect height="22" width="52" x="188" y="50">
   </rect><text x="214" y="65">
   call</text></g><path d="M240 61h10">
   </path></g><path d="M300 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 121h60">
   </path><path d="M240 121h60">
   </path><path d="M120 121h10">
   </path><g class="terminal">
   <path d="M130 121h0">
   </path><path d="M158 121h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="130" y="110">
   </rect><text x="144" y="125">
   &amp;</text></g><path d="M158 121h10">
   </path><path d="M168 121h10">
   </path><g class="non-terminal">
   <path d="M178 121h0">
   </path><path d="M230 121h0">
   </path><rect height="22" width="52" x="178" y="110">
   </rect><text x="204" y="125">
   noun</text></g><path d="M230 121h10">
   </path></g><path d="M300 121a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v100a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 151h56">
   </path><path d="M244 151h56">
   </path><path d="M116 151h10">
   </path><g class="terminal">
   <path d="M126 151h0">
   </path><path d="M162 151h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="126" y="140">
   </rect><text x="144" y="155">
   &amp;&amp;</text></g><path d="M162 151h10">
   </path><path d="M172 151h10">
   </path><g class="non-terminal">
   <path d="M182 151h0">
   </path><path d="M234 151h0">
   </path><rect height="22" width="52" x="182" y="140">
   </rect><text x="208" y="155">
   noun</text></g><path d="M234 151h10">
   </path></g><path d="M300 151a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v140a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 191h0">
   </path><path d="M300 191h0">
   </path><path d="M60 191h10">
   </path><g class="non-terminal">
   <path d="M70 191h0">
   </path><path d="M122 191h0">
   </path><rect height="22" width="52" x="70" y="180">
   </rect><text x="96" y="195">
   call</text></g><path d="M122 191h10">
   </path><g>
   <path d="M132 191h0">
   </path><path d="M300 191h0">
   </path><path d="M132 191a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M152 171h128">
   </path></g><path d="M280 171a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M132 191h20">
   </path><g>
   <path d="M152 191h0">
   </path><path d="M280 191h0">
   </path><path d="M152 191h10">
   </path><g class="terminal">
   <path d="M162 191h0">
   </path><path d="M190 191h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="162" y="180">
   </rect><text x="176" y="195">
   :</text></g><path d="M190 191h10">
   </path><path d="M200 191h10">
   </path><g class="non-terminal">
   <path d="M210 191h0">
   </path><path d="M270 191h0">
   </path><rect height="22" width="60" x="210" y="180">
   </rect><text x="240" y="195">
   guard</text></g><path d="M270 191h10">
   </path></g><path d="M280 191h20">
   </path></g></g><path d="M300 191a10 10 0 0 0 10 -10v-140a10 10 0 0 1 10 -10">
   </path></g><path d="M 320 31 h 20 m -10 -10 v 20 m 10 -20 v 20">
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
   <path d="M256 71h8">
   </path><path d="M348 71h8">
   </path><rect height="22" rx="10" ry="10" width="84" x="264" y="60">
   </rect><text x="306" y="75">
   .String.</text></g><path d="M356 71h20">
   </path><path d="M236 71a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M256 101h0">
   </path><path d="M356 101h0">
   </path><rect height="22" rx="10" ry="10" width="100" x="256" y="90">
   </rect><text x="306" y="105">
   IDENTIFIER</text></g><path d="M356 101a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
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
   <path d="M136 31h8">
   </path><path d="M228 31h8">
   </path><rect height="22" rx="10" ry="10" width="84" x="144" y="20">
   </rect><text x="186" y="35">
   .String.</text></g><path d="M236 31h20">
   </path><path d="M116 31a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M136 61h0">
   </path><path d="M236 61h0">
   </path><rect height="22" rx="10" ry="10" width="100" x="136" y="50">
   </rect><text x="186" y="65">
   IDENTIFIER</text></g><path d="M236 61a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
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
   </path><g class="terminal">
   <path d="M60 181h128">
   </path><path d="M288 181h128">
   </path><rect height="22" rx="10" ry="10" width="100" x="188" y="170">
   </rect><text x="238" y="185">
   IDENTIFIER</text></g><path d="M416 181a10 10 0 0 0 10 -10v-130a10 10 0 0 1 10 -10">
   </path><path d="M40 31a10 10 0 0 1 10 10v160a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 211h98">
   </path><path d="M318 211h98">
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
   </path></g><path d="M416 211a10 10 0 0 0 10 -10v-160a10 10 0 0 1 10 -10">
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

   <svg class="railroad-diagram" height="282" viewBox="0 0 705 282" width="705" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M664 41h0">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M408 41h0">
   </path><path d="M40 41h20">
   </path><g class="non-terminal">
   <path d="M60 41h110">
   </path><path d="M278 41h110">
   </path><rect height="22" width="108" x="170" y="30">
   </rect><text x="224" y="45">
   namePattern</text></g><path d="M388 41h20">
   </path><path d="M40 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="non-terminal">
   <path d="M60 71h106">
   </path><path d="M282 71h106">
   </path><rect height="22" width="116" x="166" y="60">
   </rect><text x="224" y="75">
   quasiLiteral</text></g><path d="M388 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 101h90">
   </path><path d="M298 101h90">
   </path><g>
   <path d="M150 101h0">
   </path><path d="M226 101h0">
   </path><path d="M150 101h20">
   </path><g class="terminal">
   <path d="M170 101h0">
   </path><path d="M206 101h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="170" y="90">
   </rect><text x="188" y="105">
   ==</text></g><path d="M206 101h20">
   </path><path d="M150 101a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M170 131h0">
   </path><path d="M206 131h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="170" y="120">
   </rect><text x="188" y="135">
   !=</text></g><path d="M206 131a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><path d="M226 101h10">
   </path><g class="non-terminal">
   <path d="M236 101h0">
   </path><path d="M288 101h0">
   </path><rect height="22" width="52" x="236" y="90">
   </rect><text x="262" y="105">
   prim</text></g><path d="M288 101h10">
   </path></g><path d="M388 101a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v100a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 161h76">
   </path><path d="M312 161h76">
   </path><path d="M136 161h10">
   </path><g class="terminal">
   <path d="M146 161h0">
   </path><path d="M174 161h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="146" y="150">
   </rect><text x="160" y="165">
   _</text></g><path d="M174 161h10">
   </path><path d="M184 161h10">
   </path><g class="terminal">
   <path d="M194 161h0">
   </path><path d="M222 161h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="194" y="150">
   </rect><text x="208" y="165">
   :</text></g><path d="M222 161h10">
   </path><path d="M232 161h10">
   </path><g class="non-terminal">
   <path d="M242 161h0">
   </path><path d="M302 161h0">
   </path><rect height="22" width="60" x="242" y="150">
   </rect><text x="272" y="165">
   guard</text></g><path d="M302 161h10">
   </path></g><path d="M388 161a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v130a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 191h0">
   </path><path d="M388 191h0">
   </path><path d="M60 191h10">
   </path><g class="terminal">
   <path d="M70 191h0">
   </path><path d="M114 191h0">
   </path><rect height="22" rx="10" ry="10" width="44" x="70" y="180">
   </rect><text x="92" y="195">
   via</text></g><path d="M114 191h10">
   </path><path d="M124 191h10">
   </path><g class="terminal">
   <path d="M134 191h0">
   </path><path d="M162 191h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="134" y="180">
   </rect><text x="148" y="195">
   (</text></g><path d="M162 191h10">
   </path><path d="M172 191h10">
   </path><g class="non-terminal">
   <path d="M182 191h0">
   </path><path d="M234 191h0">
   </path><rect height="22" width="52" x="182" y="180">
   </rect><text x="208" y="195">
   expr</text></g><path d="M234 191h10">
   </path><path d="M244 191h10">
   </path><g class="terminal">
   <path d="M254 191h0">
   </path><path d="M282 191h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="254" y="180">
   </rect><text x="268" y="195">
   )</text></g><path d="M282 191h10">
   </path><path d="M292 191h10">
   </path><g class="non-terminal">
   <path d="M302 191h0">
   </path><path d="M378 191h0">
   </path><rect height="22" width="76" x="302" y="180">
   </rect><text x="340" y="195">
   pattern</text></g><path d="M378 191h10">
   </path></g><path d="M388 191a10 10 0 0 0 10 -10v-130a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v160a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 221h30">
   </path><path d="M358 221h30">
   </path><path d="M90 221h10">
   </path><g class="terminal">
   <path d="M100 221h0">
   </path><path d="M128 221h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="100" y="210">
   </rect><text x="114" y="225">
   [</text></g><path d="M128 221h10">
   </path><path d="M138 221h10">
   </path><g>
   <path d="M148 221h0">
   </path><path d="M300 221h0">
   </path><path d="M148 221h10">
   </path><g class="non-terminal">
   <path d="M158 221h0">
   </path><path d="M290 221h0">
   </path><rect height="22" width="132" x="158" y="210">
   </rect><text x="224" y="225">
   mapPatternItem</text></g><path d="M290 221h10">
   </path><path d="M158 221a10 10 0 0 0 -10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M158 251h52">
   </path><path d="M238 251h52">
   </path><rect height="22" rx="10" ry="10" width="28" x="210" y="240">
   </rect><text x="224" y="255">
   ,</text></g><path d="M290 251a10 10 0 0 0 10 -10v-10a10 10 0 0 0 -10 -10">
   </path></g><path d="M300 221h10">
   </path><path d="M310 221h10">
   </path><g class="terminal">
   <path d="M320 221h0">
   </path><path d="M348 221h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="320" y="210">
   </rect><text x="334" y="225">
   ]</text></g><path d="M348 221h10">
   </path></g><path d="M388 221a10 10 0 0 0 10 -10v-160a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M408 41h0">
   </path><path d="M664 41h0">
   </path><path d="M408 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M428 21h216">
   </path></g><path d="M644 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M408 41h20">
   </path><g>
   <path d="M428 41h0">
   </path><path d="M644 41h0">
   </path><path d="M428 41h10">
   </path><g class="terminal">
   <path d="M438 41h0">
   </path><path d="M466 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="438" y="30">
   </rect><text x="452" y="45">
   ?</text></g><path d="M466 41h10">
   </path><path d="M476 41h10">
   </path><g class="terminal">
   <path d="M486 41h0">
   </path><path d="M514 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="486" y="30">
   </rect><text x="500" y="45">
   (</text></g><path d="M514 41h10">
   </path><path d="M524 41h10">
   </path><g class="non-terminal">
   <path d="M534 41h0">
   </path><path d="M586 41h0">
   </path><rect height="22" width="52" x="534" y="30">
   </rect><text x="560" y="45">
   expr</text></g><path d="M586 41h10">
   </path><path d="M596 41h10">
   </path><g class="terminal">
   <path d="M606 41h0">
   </path><path d="M634 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="606" y="30">
   </rect><text x="620" y="45">
   )</text></g><path d="M634 41h10">
   </path></g><path d="M644 41h20">
   </path></g></g><path d="M 664 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
   </path></g></svg>

namePattern
-----------

.. raw:: html

   <svg class="railroad-diagram" height="252" viewBox="0 0 489 252" width="489" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M448 41h0">
   </path><path d="M40 41h20">
   </path><g>
   <path d="M60 41h0">
   </path><path d="M428 41h0">
   </path><g>
   <path d="M60 41h0">
   </path><path d="M260 41h0">
   </path><path d="M60 41h20">
   </path><g>
   <path d="M80 41h0">
   </path><path d="M240 41h0">
   </path><path d="M80 41h10">
   </path><g class="terminal">
   <path d="M90 41h0">
   </path><path d="M126 41h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="90" y="30">
   </rect><text x="108" y="45">
   ::</text></g><path d="M126 41h10">
   </path><path d="M136 41h10">
   </path><g class="terminal">
   <path d="M146 41h0">
   </path><path d="M230 41h0">
   </path><rect height="22" rx="10" ry="10" width="84" x="146" y="30">
   </rect><text x="188" y="45">
   .String.</text></g><path d="M230 41h10">
   </path></g><path d="M240 41h20">
   </path><path d="M60 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M80 71h30">
   </path><path d="M210 71h30">
   </path><rect height="22" rx="10" ry="10" width="100" x="110" y="60">
   </rect><text x="160" y="75">
   IDENTIFIER</text></g><path d="M240 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path></g><g>
   <path d="M260 41h0">
   </path><path d="M428 41h0">
   </path><path d="M260 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M280 21h128">
   </path></g><path d="M408 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M260 41h20">
   </path><g>
   <path d="M280 41h0">
   </path><path d="M408 41h0">
   </path><path d="M280 41h10">
   </path><g class="terminal">
   <path d="M290 41h0">
   </path><path d="M318 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="290" y="30">
   </rect><text x="304" y="45">
   :</text></g><path d="M318 41h10">
   </path><path d="M328 41h10">
   </path><g class="non-terminal">
   <path d="M338 41h0">
   </path><path d="M398 41h0">
   </path><rect height="22" width="60" x="338" y="30">
   </rect><text x="368" y="45">
   guard</text></g><path d="M398 41h10">
   </path></g><path d="M408 41h20">
   </path></g></g><path d="M428 41h20">
   </path><path d="M40 41a10 10 0 0 1 10 10v50a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 111h32">
   </path><path d="M396 111h32">
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
   </path><path d="M396 111h0">
   </path><path d="M228 111a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M248 91h128">
   </path></g><path d="M376 91a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M228 111h20">
   </path><g>
   <path d="M248 111h0">
   </path><path d="M376 111h0">
   </path><path d="M248 111h10">
   </path><g class="terminal">
   <path d="M258 111h0">
   </path><path d="M286 111h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="258" y="100">
   </rect><text x="272" y="115">
   :</text></g><path d="M286 111h10">
   </path><path d="M296 111h10">
   </path><g class="non-terminal">
   <path d="M306 111h0">
   </path><path d="M366 111h0">
   </path><rect height="22" width="60" x="306" y="100">
   </rect><text x="336" y="115">
   guard</text></g><path d="M366 111h10">
   </path></g><path d="M376 111h20">
   </path></g></g><path d="M428 111a10 10 0 0 0 10 -10v-50a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v90a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 151h40">
   </path><path d="M388 151h40">
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
   </path><path d="M388 151h0">
   </path><path d="M220 151a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M240 131h128">
   </path></g><path d="M368 131a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M220 151h20">
   </path><g>
   <path d="M240 151h0">
   </path><path d="M368 151h0">
   </path><path d="M240 151h10">
   </path><g class="terminal">
   <path d="M250 151h0">
   </path><path d="M278 151h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="250" y="140">
   </rect><text x="264" y="155">
   :</text></g><path d="M278 151h10">
   </path><path d="M288 151h10">
   </path><g class="non-terminal">
   <path d="M298 151h0">
   </path><path d="M358 151h0">
   </path><rect height="22" width="60" x="298" y="140">
   </rect><text x="328" y="155">
   guard</text></g><path d="M358 151h10">
   </path></g><path d="M368 151h20">
   </path></g></g><path d="M428 151a10 10 0 0 0 10 -10v-90a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v120a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 181h120">
   </path><path d="M308 181h120">
   </path><path d="M180 181h10">
   </path><g class="terminal">
   <path d="M190 181h0">
   </path><path d="M226 181h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="190" y="170">
   </rect><text x="208" y="185">
   &amp;&amp;</text></g><path d="M226 181h10">
   </path><path d="M236 181h10">
   </path><g class="non-terminal">
   <path d="M246 181h0">
   </path><path d="M298 181h0">
   </path><rect height="22" width="52" x="246" y="170">
   </rect><text x="272" y="185">
   noun</text></g><path d="M298 181h10">
   </path></g><path d="M428 181a10 10 0 0 0 10 -10v-120a10 10 0 0 1 10 -10">
   </path><path d="M40 41a10 10 0 0 1 10 10v160a10 10 0 0 0 10 10">
   </path><g>
   <path d="M60 221h28">
   </path><path d="M400 221h28">
   </path><path d="M88 221h10">
   </path><g class="terminal">
   <path d="M98 221h0">
   </path><path d="M150 221h0">
   </path><rect height="22" rx="10" ry="10" width="52" x="98" y="210">
   </rect><text x="124" y="225">
   bind</text></g><path d="M150 221h10">
   </path><path d="M160 221h10">
   </path><g class="non-terminal">
   <path d="M170 221h0">
   </path><path d="M222 221h0">
   </path><rect height="22" width="52" x="170" y="210">
   </rect><text x="196" y="225">
   noun</text></g><path d="M222 221h10">
   </path><g>
   <path d="M232 221h0">
   </path><path d="M400 221h0">
   </path><path d="M232 221a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M252 201h128">
   </path></g><path d="M380 201a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M232 221h20">
   </path><g>
   <path d="M252 221h0">
   </path><path d="M380 221h0">
   </path><path d="M252 221h10">
   </path><g class="terminal">
   <path d="M262 221h0">
   </path><path d="M290 221h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="262" y="210">
   </rect><text x="276" y="225">
   :</text></g><path d="M290 221h10">
   </path><path d="M300 221h10">
   </path><g class="non-terminal">
   <path d="M310 221h0">
   </path><path d="M370 221h0">
   </path><rect height="22" width="60" x="310" y="210">
   </rect><text x="340" y="225">
   guard</text></g><path d="M370 221h10">
   </path></g><path d="M380 221h20">
   </path></g></g><path d="M428 221a10 10 0 0 0 10 -10v-160a10 10 0 0 1 10 -10">
   </path></g><path d="M 448 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
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

   <svg class="railroad-diagram" height="200" viewBox="0 0 593 200" width="593" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
   <g transform="translate(.5 .5)">
   <path d="M 20 31 v 20 m 10 -20 v 20 m -10 -10 h 20.5">
   </path><g>
   <path d="M40 41h0">
   </path><path d="M552 41h0">
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
   </path><path d="M504 41h0">
   </path><path d="M228 41a10 10 0 0 0 10 -10v0a10 10 0 0 1 10 -10">
   </path><g>
   <path d="M248 21h236">
   </path></g><path d="M484 21a10 10 0 0 1 10 10v0a10 10 0 0 0 10 10">
   </path><path d="M228 41h20">
   </path><g>
   <path d="M248 41h0">
   </path><path d="M484 41h0">
   </path><path d="M248 41h10">
   </path><g>
   <path d="M258 41h0">
   </path><path d="M474 41h0">
   </path><path d="M258 41h20">
   </path><g class="terminal">
   <path d="M278 41h66">
   </path><path d="M388 41h66">
   </path><rect height="22" rx="10" ry="10" width="44" x="344" y="30">
   </rect><text x="366" y="45">
   ...</text></g><path d="M454 41h20">
   </path><path d="M258 41a10 10 0 0 1 10 10v10a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M278 71h54">
   </path><path d="M400 71h54">
   </path><rect height="22" rx="10" ry="10" width="68" x="332" y="60">
   </rect><text x="366" y="75">
   $IDENT</text></g><path d="M454 71a10 10 0 0 0 10 -10v-10a10 10 0 0 1 10 -10">
   </path><path d="M258 41a10 10 0 0 1 10 10v40a10 10 0 0 0 10 10">
   </path><g>
   <path d="M278 101h0">
   </path><path d="M454 101h0">
   </path><path d="M278 101h10">
   </path><g class="terminal">
   <path d="M288 101h0">
   </path><path d="M324 101h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="288" y="90">
   </rect><text x="306" y="105">
   ${</text></g><path d="M324 101h10">
   </path><path d="M334 101h10">
   </path><g class="non-terminal">
   <path d="M344 101h0">
   </path><path d="M396 101h0">
   </path><rect height="22" width="52" x="344" y="90">
   </rect><text x="370" y="105">
   expr</text></g><path d="M396 101h10">
   </path><path d="M406 101h10">
   </path><g class="terminal">
   <path d="M416 101h0">
   </path><path d="M444 101h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="416" y="90">
   </rect><text x="430" y="105">
   }</text></g><path d="M444 101h10">
   </path></g><path d="M454 101a10 10 0 0 0 10 -10v-40a10 10 0 0 1 10 -10">
   </path><path d="M258 41a10 10 0 0 1 10 10v70a10 10 0 0 0 10 10">
   </path><g class="terminal">
   <path d="M278 131h54">
   </path><path d="M400 131h54">
   </path><rect height="22" rx="10" ry="10" width="68" x="332" y="120">
   </rect><text x="366" y="135">
   @IDENT</text></g><path d="M454 131a10 10 0 0 0 10 -10v-70a10 10 0 0 1 10 -10">
   </path><path d="M258 41a10 10 0 0 1 10 10v100a10 10 0 0 0 10 10">
   </path><g>
   <path d="M278 161h0">
   </path><path d="M454 161h0">
   </path><path d="M278 161h10">
   </path><g class="terminal">
   <path d="M288 161h0">
   </path><path d="M324 161h0">
   </path><rect height="22" rx="10" ry="10" width="36" x="288" y="150">
   </rect><text x="306" y="165">
   @{</text></g><path d="M324 161h10">
   </path><path d="M334 161h10">
   </path><g class="non-terminal">
   <path d="M344 161h0">
   </path><path d="M396 161h0">
   </path><rect height="22" width="52" x="344" y="150">
   </rect><text x="370" y="165">
   expr</text></g><path d="M396 161h10">
   </path><path d="M406 161h10">
   </path><g class="terminal">
   <path d="M416 161h0">
   </path><path d="M444 161h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="416" y="150">
   </rect><text x="430" y="165">
   }</text></g><path d="M444 161h10">
   </path></g><path d="M454 161a10 10 0 0 0 10 -10v-100a10 10 0 0 1 10 -10">
   </path></g><path d="M474 41h10">
   </path><path d="M258 41a10 10 0 0 0 -10 10v119a10 10 0 0 0 10 10">
   </path><g>
   <path d="M258 180h216">
   </path></g><path d="M474 180a10 10 0 0 0 10 -10v-119a10 10 0 0 0 -10 -10">
   </path></g><path d="M484 41h20">
   </path></g><path d="M504 41h10">
   </path><g class="terminal">
   <path d="M514 41h0">
   </path><path d="M542 41h0">
   </path><rect height="22" rx="10" ry="10" width="28" x="514" y="30">
   </rect><text x="528" y="45">
   `</text></g><path d="M542 41h10">
   </path></g><path d="M 552 41 h 20 m -10 -10 v 20 m 10 -20 v 20">
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
