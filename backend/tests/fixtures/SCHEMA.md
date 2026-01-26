# Astrology Chart JSON Schema – v1

{
  meta: object,
  vedic: object,
  western: object,
  chinese: object,
  vimshottari_dasha: object,
  transits_2026: object
}




meta: {
  name: string,
  birth_date: string (YYYY-MM-DD),
  birth_time: string (HH:MM:SS),
  birth_place: string,
  latitude: number,
  longitude: number,
  timezone_offset: number,
  julian_day: number,
  generated_at: string (ISO timestamp)
}




vedic: {
  ayanamsa: number,
  ayanamsa_type: string,
  ascendant: object,
  planets: object
}




ascendant: {
  longitude: number,
  longitude_dms: string,
  nakshatra: object,
  rashi: object
}




planets: {
  sun: planet_object,
  moon: planet_object,
  mars: planet_object,
  mercury: planet_object,
  jupiter: planet_object,
  venus: planet_object,
  saturn: planet_object,
  rahu: planet_object,
  ketu: planet_object
}




planet_object: {
  name: string,
  longitude: number,
  longitude_dms: string,
  retrograde: boolean,
  nakshatra: object,
  rashi: object
}


western: {
  ascendant: object,
  planets: object
}






planets: {
  sun: object,
  moon: object,
  mars: object,
  mercury: object,
  jupiter: object,
  venus: object,
  saturn: object,
  uranus?: object,
  neptune?: object,
  pluto?: object
}



chinese: {
  animal: string,
  element: string,
  yin_yang: string,
  full: string,
  year: number
}



vimshottari_dasha: {
  starting_dasha: string,
  moon_nakshatra: string,
  current_dasha: string,
  periods: [
    {
      planet: string,
      start: string (YYYY-MM-DD),
      end: string (YYYY-MM-DD)
    }
  ]
}



transits_2026: {
  mercury_retrogrades: [
    { start: string, end: string, sign: string }
  ],
  major_transits: [
    { date: string, event: string }
  ],
  eclipses: [
    { date: string, type: string, sign: string }
  ],
  chinese_year: {
    starts: string,
    animal: string,
    element: string,
    full: string
  }
}



