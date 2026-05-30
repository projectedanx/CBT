import { TestBed } from '@angular/core/testing';
import { SymbioticTensorMesh } from './tensor-mesh.service';

describe('SymbioticTensorMesh', () => {
  let service: SymbioticTensorMesh;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SymbioticTensorMesh);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('calculateGravity', () => {
    it('should map a CRS of 0 to the baseline gravity constant', () => {
      // Assuming a baseline G of 0.1
      expect(service.calculateGravity(0)).toBeCloseTo(0.1, 4);
    });

    it('should scale gravity exponentially for high CRS values to enforce topological bounds', () => {
      // Golden ratio constraint: A CRS of 100 should apply max repulsion/attraction
      const g0 = service.calculateGravity(0);
      const g50 = service.calculateGravity(50);
      const g100 = service.calculateGravity(100);

      expect(g50).toBeGreaterThan(g0);
      expect(g100).toBeGreaterThan(g50);
      expect(g100).toBeCloseTo(0.1 * 1.618, 4); // Φ = 1.618
    });

    it('should handle boundary values safely', () => {
      expect(service.calculateGravity(-10)).toBe(service.calculateGravity(0));
      expect(service.calculateGravity(150)).toBe(service.calculateGravity(100));
    });
  });
});
