<script>
  import { setContext, getContext } from 'svelte';
  import { writable, derived } from 'svelte/store';
  import MenuLayer from './mapping/MenuLayer.svelte';
  import PixiLayer from './PixiLayer.svelte';

  // @TODO: make read-only accessors for components that should not write??
  // --- Component properties
  export let dataKey = null;
  const { nodeTitles, edgeTitles } = getContext(dataKey);

  // --- Node mapping context
  const nodeMappingKey = {};
  setContext(nodeMappingKey, {
    mapColor: writable(false),
    colorType: writable('seq'),
    colorScale: writable((x) => x),
    mapSize: writable(false),
    sizeScale: writable((x) => x),
    sizeTitle: derived(nodeTitles, ($nodeTitles) => $nodeTitles.size),
    colorTitle: derived(nodeTitles, ($nodeTitles) => $nodeTitles.color)
  });

  // --- Edge mapping context
  const edgeMappingKey = {};
  setContext(edgeMappingKey, {
    mapColor: writable(false),
    colorType: writable('seq'),
    colorScale: writable((x) => x),
    mapSize: writable(false),
    sizeScale: writable((x) => x),
    sizeTitle: derived(edgeTitles, ($edgeTitles) => $edgeTitles.size),
    colorTitle: derived(edgeTitles, ($edgeTitles) => $edgeTitles.color)
  });

  // --- Encoding context
  const encodingKey = {};
  setContext(encodingKey, {
    progress: writable(0),
    nodePositions: writable([]),
    nodeColors: writable([]),
    nodeRadii: writable([]),
    edgeColors: writable([]),
    edgeWidths: writable([]),
    edgeAlpha: writable(0.1),
    moveNode: writable(() => {})
  });
</script>

<PixiLayer
  dataKey={dataKey}
  encodingKey={encodingKey}
  edgeMappingKey={edgeMappingKey}
  nodeMappingKey={nodeMappingKey} />
<MenuLayer
  dataKey={dataKey}
  encodingKey={encodingKey}
  edgeMappingKey={edgeMappingKey}
  nodeMappingKey={nodeMappingKey} />
