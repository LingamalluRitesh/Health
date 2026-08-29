/**
 * HealthPulse AI — TypeScript SDK FHIR R4 Helpers.
 */

export interface FHIRCoding {
  system?: string;
  code?: string;
  display?: string;
}

export interface FHIRCodeableConcept {
  coding?: FHIRCoding[];
  text?: string;
}

export interface FHIRResource {
  resourceType: string;
  id: string;
  [key: string]: any;
}

export function createObservationResource(
  patientId: string,
  loincCode: string,
  display: string,
  value: number,
  unit: string
): FHIRResource {
  return {
    resourceType: "Observation",
    id: `obs-${Date.now()}`,
    status: "final",
    code: {
      coding: [{ system: "http://loinc.org", code: loincCode, display }],
      text: display,
    },
    subject: {
      reference: `Patient/${patientId}`,
      type: "Patient",
    },
    effectiveDateTime: new Date().toISOString(),
    valueQuantity: {
      value,
      unit,
      system: "http://unitsofmeasure.org",
      code: unit,
    },
  };
}
