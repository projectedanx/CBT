import { Component, ElementRef, Input, OnChanges, SimpleChanges, ViewChild, ViewEncapsulation } from '@angular/core';
import * as d3 from 'd3';
import { GraphData, ConceptNode, ConceptLink } from '../types';

/**
 * Interface augmenting the base ConceptNode with required properties for D3's Force Simulation mechanics.
 */
interface SimulationNode extends ConceptNode, d3.SimulationNodeDatum {}

/**
 * Interface augmenting the base ConceptLink with required properties for D3's Force Simulation mechanics.
 */
interface SimulationLink extends d3.SimulationLinkDatum<SimulationNode> {
  value: number;
}

/**
 * Visual topology component responsible for projecting the Conceptual Blending Theory geometry.
 * Bridges declarative Angular data-binding with imperative D3 force-directed physics simulations.
 */
@Component({
  selector: 'app-concept-graph',
  standalone: true,
  template: `
    <div #graphContainer class="w-full h-full bg-slate-900 rounded-lg overflow-hidden border border-slate-700 shadow-inner relative">
      @if (data.nodes.length === 0) {
        <div class="absolute inset-0 flex items-center justify-center text-slate-500 font-mono text-sm">
          Awaiting Cognitive Input...
        </div>
      }
    </div>
  `,
  styles: [`
    .node text {
      pointer-events: none;
      text-shadow: 0 1px 0 #000, 1px 0 0 #000, 0 -1px 0 #000, -1px 0 0 #000;
    }
  `],
  encapsulation: ViewEncapsulation.None
})
export class ConceptGraphComponent implements OnChanges {
  /** The abstract conceptual topology provided by the cognitive engine. */
  @Input({ required: true }) data!: GraphData;
  /** The structural DOM hook used to anchor the SVG simulation. */
  @ViewChild('graphContainer') container!: ElementRef;

  /** The active D3 force simulation engine dictating node placement. */
  private simulation: d3.Simulation<SimulationNode, SimulationLink> | null = null;
  /** The root SVG selection context. */
  private svg: any;

  /**
   * Intercepts declarative data mutations from the host environment to trigger imperative graph re-renders.
   *
   * @param {SimpleChanges} changes - The delta payload containing previous and current topological data.
   */
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['data'] && this.data.nodes.length > 0) {
      this.renderGraph();
    }
  }

  /**
   * Teardown and reconstruction sequence for the D3 physics simulation.
   * Establishes the force vectors, gravitational centers, and aesthetic mappings for the new topology.
   */
  private renderGraph(): void {
    if (!this.container) return;

    const element = this.container.nativeElement;
    // Clear previous
    d3.select(element).selectAll('*').remove();

    const width = element.clientWidth;
    const height = element.clientHeight || 500;

    this.svg = d3.select(element)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', [0, 0, width, height]);

    // Color scale based on group
    const color = (d: ConceptNode) => {
        switch(d.type) {
            case 'input-a': return '#3b82f6'; // blue-500
            case 'input-b': return '#ef4444'; // red-500
            case 'generic': return '#a855f7'; // purple-500
            case 'blend': return '#10b981';   // emerald-500
            default: return '#cbd5e1';
        }
    };

    // Prepare data for D3 (Clone to avoid mutating Inputs and satisfy types)
    const nodes: SimulationNode[] = this.data.nodes.map(d => ({ ...d }));
    const links: SimulationLink[] = this.data.links.map(d => ({ ...d }));

    // Simulation setup
    this.simulation = d3.forceSimulation<SimulationNode>(nodes)
      .force('link', d3.forceLink<SimulationNode, SimulationLink>(links).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collide', d3.forceCollide(40));

    // Links
    const link = this.svg.append('g')
      .attr('stroke', '#475569')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke-width', (d: any) => Math.sqrt(d.value || 1) * 1.5);

    // Nodes
    const node = this.svg.append('g')
      .selectAll('g')
      .data(nodes)
      .join('g')
      .call(d3.drag<SVGGElement, SimulationNode>()
        .on('start', (event, d) => {
          if (!event.active) this.simulation?.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on('drag', (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on('end', (event, d) => {
          if (!event.active) this.simulation?.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }));

    // Node Circles
    node.append('circle')
      .attr('r', (d: SimulationNode) => d.type === 'blend' ? 12 : 8)
      .attr('fill', (d: SimulationNode) => color(d))
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5);

    // Node Labels
    node.append('text')
      .text((d: SimulationNode) => d.label)
      .attr('x', 14)
      .attr('y', 4)
      .attr('fill', '#e2e8f0')
      .attr('font-size', '12px')
      .attr('font-family', 'monospace')
      .attr('font-weight', 'bold')
      .style('pointer-events', 'none'); // Ensure text doesn't interfere with drag

    this.simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('transform', (d: any) => `translate(${d.x},${d.y})`);
    });
  }

  /**
   * Serializes the active D3 topology SVG and triggers a browser download.
   * This physicalizes the Golden Scar Protocol by allowing the operator to freeze and capture
   * the high-entropy conceptual geometry generated by the AI before it collapses.
   *
   * @param {string} filename - The desired name of the exported SVG file.
   */
  exportSVG(filename: string = 'conceptual-blend.svg'): void {
    if (!this.svg) return;

    const svgNode = this.svg.node();
    if (!svgNode) return;

    const serializer = new XMLSerializer();
    let source = serializer.serializeToString(svgNode);

    // Add namespace if missing
    if (!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)) {
        source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
    }
    // Add xml declaration
    source = '<?xml version="1.0" standalone="no"?>\r\n' + source;

    const url = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(source);

    const downloadLink = document.createElement("a");
    downloadLink.href = url;
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  }
}
