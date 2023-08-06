<script>
  import { setContext } from 'svelte';
  import { derived, writable } from 'svelte/store';
  import { createReadableValue, createWritableValue } from './util/stores';
  import NeighbourMap from './components/NeighbourMap.svelte';
  import EncodingLayer from './components/EncodingLayer.svelte';
  import html2canvas from 'html2canvas';

  // --- Component properties
  export let model;
  let el;

  // --- Global context
  const dataKey = {};
  // The current communication-schema between server and client does not consider
  // partial updates to the network. All aspects of the network are updated in the
  // client, even when only (f.i.) the node-color data changed...
  const network = createReadableValue(model, 'network');
  const featureMode = createReadableValue(model, 'featureMode');
  const selectedNodes = createWritableValue(model, 'selectedNodes');
  const selectedNodesOther = createReadableValue(model, 'selectedNodesOther');
  const takeScreenshot = createWritableValue(model, 'takeScreenshot');
  const screenshot = createWritableValue(model, 'screenshot');
  const nodeTitles = createReadableValue(model, 'nodeTitles');
  const edgeTitles = createReadableValue(model, 'linkTitles');
  const render = writable(() => {});

  setContext(dataKey, {
    nodes: derived(network, () => $network[0]),
    edges: derived(network, () => $network[1]),
    selectedNodes: selectedNodes,
    selectedNodesOther: selectedNodesOther,
    featureMode: featureMode,
    neighbours: writable({}),
    render,
    nodeTitles,
    edgeTitles
  });

  $: if ($takeScreenshot) {
    if (el) {
      $render();
      html2canvas(el).then((canvas) => {
        $screenshot = canvas.toDataURL();
      });
    }
    $takeScreenshot = false;
  }
</script>

<div id="stad-widget-main" bind:this={el}>
  <EncodingLayer dataKey={dataKey} />
  <NeighbourMap dataKey={dataKey} />
</div>
<br />

<style>
  #stad-widget-main {
    /*width: 100%;*/
    margin: 5px;
    position: relative;
  }
</style>
