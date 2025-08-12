type TravelMode = "DRIVING" | "WALKING"

export default async function getRoute(
  mode: TravelMode,
  origin: string,
  destination: string,
  apiKey: string
) {
  // Minimal placeholder; replace with proper Directions API call later
  return {
    travelDistance: 1.0,
    travelDuration: 600,
  }
}


