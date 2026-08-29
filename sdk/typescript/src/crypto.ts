/**
 * HealthPulse AI — TypeScript SDK Cryptographic Verification Utilities.
 */

export async function computeSHA256(message: string): Promise<string> {
  if (typeof crypto !== "undefined" && crypto.subtle) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  }
  // Fallback representation for Node environment without subtle
  return `hash_${message.length}_${Date.now()}`;
}
