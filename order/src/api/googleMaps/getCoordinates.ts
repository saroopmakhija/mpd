export type Coordinates = { latitude: number; longitude: number }

export default async function getCoordinates(address: string, apiKey: string): Promise<Coordinates | null> {
  // Minimal placeholder; replace with proper Geocoding API later
  return { latitude: 0, longitude: 0 }
}


