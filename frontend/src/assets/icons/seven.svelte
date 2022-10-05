<script lang="ts">
    export let color: string | undefined;
    export let height: string | undefined;
    export let width: string | undefined;
</script>
<svg height={height} width={width} version="1.1" viewBox="0 0 242 362" xmlns="http://www.w3.org/2000/svg">
 <g transform="translate(-419 748.64)">
  <g transform="matrix(4 0 0 4 -1260 -2077.1)" fill-rule="evenodd">
   <rect x="420" y="332.36" width="60" height="90" rx="10" ry="10" fill="#fff" stroke="#000" stroke-width=".5"/>
   <rect x="425" y="337.36" width="50" height="80" rx="5" ry="5" fill={color}/>
   <path d="m465 352.36c-22.091 0-40 17.909-40 40 0 5.5228 4.4772 10 10 10 22.091 0 40-17.909 40-40 0-5.5228-4.4772-10-10-10z" fill="#fff"/>
   <path d="m441.5 362.36v10h5v-5h10l-10 25h5l10-25v-5h-15z" fill={color}/>
   <path d="m427.5 339.86v5h2.5v-2.5h5l-5 12.5h2.5l5-12.5v-2.5h-7.5z" fill="#fff"/>
   <path d="m472.5 414.86v-5h-2.5v2.5h-5l5-12.5h-2.5l-5 12.5v2.5h7.5z" fill="#fff"/>
  </g>
 </g>
</svg>
