<script>
  // --- Component props
  export let scale = null;
  export let width = 320;
  export let height = 45;
  export let tickFormat = (x) => x;
  export let swatchSize = 15;
  export let swatchwidth = swatchSize;
  export let swatchHeight = swatchSize;
  export let swatchPadding = 5;
  export let marginTop = 5;
  export let marginLeft = 0;
  export let title = null;
  export let titleSize = 10;

  // --- Reactive part
  $: domain = $scale.domain();

  function fill(c) {
    return $scale(c);
  }

  // TODO: Wrap swatches when num categories increases.
  // Or just ignore it, as more than 12 categories is bad anyway...
</script>

<svg
  class="color-swatches"
  height={height}
  viewBox={[0, 0, width, height]}
  width={width}>
  <g transform={`translate(0, ${titleSize})`}>
    <text style="font-size: 10; font-family: sans-serif;">{$title}</text>
  </g>
  <g>
    {#each domain as cat, i}
      <rect
        x={marginLeft + i * (swatchwidth + swatchPadding)}
        y={marginTop + titleSize}
        width={swatchwidth}
        height={swatchHeight}
        style={`fill: ${fill(cat)};`} />
      <text
        x={marginLeft + i * (swatchwidth + swatchPadding) + swatchwidth / 2}
        y={marginTop + titleSize + swatchHeight + swatchPadding}
        font-size="10"
        font-family="sans-serif"
        text-anchor="middle"
        dominant-baseline="hanging">
        {tickFormat(cat)}
      </text>
    {/each}
  </g>
</svg>

<style>
  .color-swatches {
    overflow: visible;
    display: block;
  }
</style>
