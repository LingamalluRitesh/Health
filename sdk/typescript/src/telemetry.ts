/**
 * HealthPulse AI — TypeScript WebSocket Telemetry Stream Client.
 */

import { PatientVitalSigns } from "./types.js";

export type TelemetryCallback = (vitals: PatientVitalSigns) => void;

export class TelemetryStreamClient {
  private wsUrl: string;
  private ws: WebSocket | null = null;
  private subscribers: TelemetryCallback[] = [];

  constructor(wsBaseUrl: string, patientId: string) {
    const cleanUrl = wsBaseUrl.replace(/^http/, "ws").replace(/\/$/, "");
    this.wsUrl = `${cleanUrl}/ws/telemetry/${patientId}`;
  }

  public connect() {
    if (typeof WebSocket === "undefined") return;
    this.ws = new WebSocket(this.wsUrl);

    this.ws.onmessage = (event) => {
      try {
        const data: PatientVitalSigns = JSON.parse(event.data);
        this.subscribers.forEach((cb) => cb(data));
      } catch (err) {
        console.error("Failed to parse vital telemetry packet", err);
      }
    };
  }

  public onVitalUpdate(callback: TelemetryCallback) {
    this.subscribers.push(callback);
  }

  public disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
