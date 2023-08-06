<script>
  import { getContext } from 'svelte';
  import Swatches from './Swatches.svelte';
  import ColorLegend from './ColorLegend.svelte';
  import SizeLegend from './SizeLegends.svelte';

  // --- Component Props
  export let renderKey = null;
  export let nodeMappingKey = null;
  export let edgeMappingKey = null;

  // // --- Get context
  const { viewport } = getContext(renderKey);

  const nodeMapping = getContext(nodeMappingKey);
  const nodeMapColor = nodeMapping.mapColor;
  const nodeColorType = nodeMapping.colorType;
  const nodeColorScale = nodeMapping.colorScale;
  const nodeMapSize = nodeMapping.mapSize;
  const nodeSizeScale = nodeMapping.sizeScale;
  const nodeColorTitle = nodeMapping.colorTitle;
  const nodeSizeTitle = nodeMapping.sizeTitle;

  const edgeMapping = getContext(edgeMappingKey);
  const edgeMapColor = edgeMapping.mapColor;
  const edgeColorType = edgeMapping.colorType;
  const edgeColorScale = edgeMapping.colorScale;
  const edgeMapSize = edgeMapping.mapSize;
  const edgeSizeScale = edgeMapping.sizeScale;
  const edgeColorTitle = edgeMapping.colorTitle;
  const edgeSizeTitle = edgeMapping.sizeTitle;
</script>

<div id="legends-container">
  {#if $nodeMapColor}
    {#if $nodeColorType === 'cat'}
      <Swatches scale={nodeColorScale} title={nodeColorTitle} />
    {:else}
      <ColorLegend scale={nodeColorScale} title={nodeColorTitle} />
    {/if}
  {/if}

  {#if $nodeMapSize}
    <SizeLegend
      scale={nodeSizeScale}
      shape="circle"
      viewport={viewport}
      title={nodeSizeTitle} />
  {/if}

  {#if $edgeMapColor}
    {#if $edgeColorType === 'cat'}
      <Swatches scale={edgeColorScale} title={edgeColorTitle} />
    {:else}
      <ColorLegend scale={edgeColorScale} title={edgeColorTitle} />
    {/if}
  {/if}

  {#if $edgeMapSize}
    <SizeLegend
      scale={edgeSizeScale}
      shape="line"
      viewport={viewport}
      title={edgeSizeTitle} />
  {/if}
</div>

<style>
  #legends-container {
    position: absolute;
    top: 10px;
    left: 230px;
    display: flex;
    flex-direction: column;
    width: 320px;
    color: rgb(50, 50, 50);
  }
</style>
