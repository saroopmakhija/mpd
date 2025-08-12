export default function getMapsApiKey() {
    return process.env.GOOGLE_MAPS_API_KEY || "dummy"
}