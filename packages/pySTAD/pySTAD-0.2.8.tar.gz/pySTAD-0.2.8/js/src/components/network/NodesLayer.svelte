<script>
  import { getContext, setContext } from 'svelte';
  import { Container } from 'pixi.js';
  import Node from './Node.svelte';

  // --- Component properties
  export let dataKey = null;
  export let renderKey = null;
  export let encodingKey = null;
  export let hoverAlpha = 0.2;
  export let tooltipOffset = { x: 10, y: 10 };

  // --- Context
  const { nodes, neighbours } = getContext(dataKey);
  const { viewport, requestRender } = getContext(renderKey);
  const { nodePositions } = getContext(encodingKey);

  // --- Graphics objects
  const nodesLayerKey = {};
  const nodesLayer = new Container();
  const frontLayer = new Container();
  const nodesMap = {};

  viewport.addChild(nodesLayer);
  viewport.addChild(frontLayer);

  setContext(nodesLayerKey, {
    nodesLayer: nodesLayer,
    frontLayer: frontLayer,
    nodesMap: nodesMap
  });

  // --- Hover state

  let hoverNodeIndices = null;
  let hoverId = null;
  let showTooltip = false;
  let tooltipCoords = { x: 0, y: 0 };
  let tooltipText = '';

  function handleHoverStart(event) {
    const { id, originalEvent } = event.detail;

    if ($neighbours) {
      hoverNodeIndices = [...$neighbours.get(id), id];
      moveNodesToLayer(hoverNodeIndices, nodesLayer, frontLayer);
      nodesLayer.alpha = hoverAlpha;
    }

    const rect = originalEvent.target.getBoundingClientRect();
    const pos = {
      x: originalEvent.clientX - rect.left,
      y: originalEvent.clientY - rect.top
    };
    updateTooltip(id, pos);
    requestRender();
  }

  // eslint-disable-next-line no-unused-vars
  function handleHoverEnd(_) {
    if (hoverNodeIndices) {
      moveNodesToLayer(hoverNodeIndices, frontLayer, nodesLayer);
      hoverNodeIndices = null;
    }

    // Undo fade and tooltip
    showTooltip = false;
    nodesLayer.alpha = 1;
    requestRender();
  }

  function moveNodesToLayer(nodeIndices, removeLayer, addLayer) {
    // Fairly bad complexity here...
    for (const id of nodeIndices) {
      const nodeGfx = nodesMap[id];
      removeLayer.removeChild(nodeGfx);
      addLayer.addChild(nodeGfx);
    }
  }

  function updateTooltip(id, pos) {
    tooltipText = $nodes[id].label;
    tooltipCoords.x = pos.x + tooltipOffset.x;
    tooltipCoords.y = pos.y + tooltipOffset.y;
    showTooltip = true;
  }
</script>

{#if showTooltip}
  <span
    class="tooltiptext"
    style="top: {tooltipCoords.y}px; left: {tooltipCoords.x}px">
    {tooltipText}
  </span>
{/if}

<!-- Is ID always the same as the index? -->
{#each $nodes as { id }}
  <Node
    id={id}
    dataKey={dataKey}
    renderKey={renderKey}
    encodingKey={encodingKey}
    nodesLayerKey={nodesLayerKey}
    on:hoverStart={handleHoverStart}
    on:hoverEnd={handleHoverEnd} />
{/each}

<style>
  .tooltiptext {
    position: absolute;
    background-color: #555;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 0 2px 0 2px;
    z-index: 1;
  }
</style>
