// PCOS Copilot Frontend Mock API Service
// ----------------------------------------------------
// TODO: When connecting to the backend, replace these mock calls with actual
// fetch/axios calls to your FastAPI/Express/Node.js endpoints.

export interface SymptomLog {
  date: string;
  acne: string; // "None" | "Mild" | "Moderate" | "Severe"
  fatigue: string; // "None" | "Mild" | "Moderate" | "Severe"
  bloating: string; // "None" | "Mild" | "Moderate" | "Severe"
  cramps: string; // "None" | "Mild" | "Moderate" | "Severe"
  mood: string; // "Good" | "Anxious" | "Depressed" | "Irritable"
  cravings: string; // "None" | "Sweet" | "Salty" | "Carbs"
}

export interface LabMarker {
  id: string;
  name: string;
  category: string;
  value: number;
  unit: string;
  status: "Normal" | "Borderline" | "High" | "Low";
  explanation: string;
  detailedExplanation: string;
}

export interface CycleData {
  currentDay: number;
  totalDays: number;
  phase: "Follicular" | "Ovulatory" | "Luteal" | "Menstrual";
  phaseRemainingDays: number;
  estrogen: number;
  progesterone: number;
  lh: number;
  fsh: number;
}

export interface CoachMessage {
  id: string;
  sender: "user" | "coach";
  text: string;
  timestamp: string;
}

export interface ProfileData {
  name: string;
  age: number;
  diagnosedYear: string;
  height: string;
  weight: string;
  healthGoals: string[];
  wearableConnected: boolean;
  wearableType: string;
}

// Initial Mock Data
let mockSymptoms: SymptomLog[] = [
  { date: "2026-06-21", acne: "Mild", fatigue: "Moderate", bloating: "Mild", cramps: "None", mood: "Good", cravings: "Sweet" },
  { date: "2026-06-22", acne: "Mild", fatigue: "Moderate", bloating: "None", cramps: "None", mood: "Anxious", cravings: "Carbs" },
  { date: "2026-06-23", acne: "Moderate", fatigue: "Mild", bloating: "Mild", cramps: "None", mood: "Irritable", cravings: "Sweet" },
  { date: "2026-06-24", acne: "Mild", fatigue: "Moderate", bloating: "Moderate", cramps: "None", mood: "Good", cravings: "None" }
];

let mockLabMarkers: LabMarker[] = [
  {
    id: "lh",
    name: "Luteinizing Hormone (LH)",
    category: "Hormone Marker",
    value: 14.2,
    unit: "mIU/mL",
    status: "High",
    explanation: "Elevated LH is common in PCOS. An LH:FSH ratio greater than 2:1 often suggests hormonal imbalance that can affect ovulation cycles.",
    detailedExplanation: "High LH relative to FSH is a classic hallmark of PCOS. In healthy cycles, LH surges only right before ovulation, but in PCOS, it can remain chronically elevated, causing follicle development to stall and cycles to be delayed."
  },
  {
    id: "fsh",
    name: "Follicle Stimulating (FSH)",
    category: "Hormone Marker",
    value: 5.1,
    unit: "mIU/mL",
    status: "Normal",
    explanation: "Your FSH level is within the healthy follicular phase range. However, the ratio compared to LH is the key indicator for PCOS assessment.",
    detailedExplanation: "Your pituitary gland is secreting FSH normally to mature ovarian follicles. However, because LH is disproportionately high, the ovaries receive confused signals, leading to irregular ovulation."
  },
  {
    id: "amh",
    name: "Anti-Müllerian (AMH)",
    category: "Fertility Marker",
    value: 6.8,
    unit: "ng/mL",
    status: "Borderline",
    explanation: "AMH levels reflect egg reserve. High levels (above 5 ng/mL) are frequently seen in women with PCOS due to multiple small follicles.",
    detailedExplanation: "AMH is produced by the granulosa cells in ovarian follicles. High AMH levels are associated with polycystic ovaries because the large number of small, undeveloped follicles each produce AMH, preventing a single dominant follicle from growing and ovulating."
  },
  {
    id: "testosterone",
    name: "Total Testosterone",
    category: "Androgen Marker",
    value: 78,
    unit: "ng/dL",
    status: "High",
    explanation: "Hyperandrogenism is a core diagnostic pillar of PCOS. Elevated levels can contribute to symptoms like acne or hair thinning.",
    detailedExplanation: "High testosterone levels drive many physical symptoms of PCOS, including hirsutism (excess facial/body hair), hormonal acne, and androgenic alopecia. Managing insulin levels is key to lowering ovarian testosterone production."
  },
  {
    id: "insulin",
    name: "Fasting Insulin",
    category: "Metabolic Marker",
    value: 12.5,
    unit: "µIU/mL",
    status: "Borderline",
    explanation: "Your insulin is within clinical 'normal' but above the 'optimal' range (<7) for metabolic health in PCOS management.",
    detailedExplanation: "Fasting insulin above 7 µIU/mL suggests early-stage insulin resistance. When cells become resistant to insulin, the pancreas produces more, and excess insulin stimulates the ovaries to produce more testosterone, worsening PCOS."
  }
];

let mockCycleData: CycleData = {
  currentDay: 6,
  totalDays: 28,
  phase: "Follicular",
  phaseRemainingDays: 6,
  estrogen: 120,
  progesterone: 0.8,
  lh: 8.5,
  fsh: 6.2
};

let mockMessages: CoachMessage[] = [
  {
    id: "1",
    sender: "coach",
    text: "Hello Sarah! I've been reviewing your recent cycle logs and hormone reports. It looks like we have some new data to discuss. What's on your mind?",
    timestamp: "10:00 AM"
  },
  {
    id: "2",
    sender: "user",
    text: "I've been feeling more fatigued than usual this week. Could it be related to my insulin levels?",
    timestamp: "10:02 AM"
  },
  {
    id: "3",
    sender: "coach",
    text: "It's very possible. Fatigue in PCOS is often linked to insulin resistance, which can cause blood sugar fluctuations throughout the day. Based on your recent logs, you have noted an afternoon energy dip 4 times this week, and you logged a high carb intake during lunch. Try incorporating more protein into your breakfast tomorrow and see if that stabilizes your energy levels. Would you like a meal suggestion?",
    timestamp: "10:03 AM"
  }
];

let mockProfile: ProfileData = {
  name: "Sarah Jenkins",
  age: 26,
  diagnosedYear: "2024",
  height: "165 cm",
  weight: "68 kg",
  healthGoals: ["Regulate Cycle", "Manage Insulin Resistance", "Clear Skin"],
  wearableConnected: true,
  wearableType: "Apple Watch Series 9"
};

// API Services
export const apiService = {
  // ----------------------------------------------------
  // Dashboard Data
  // ----------------------------------------------------
  getDashboardData: async () => {
    // Fetch real cycle data from the new endpoint
    const cycleData = await apiService.getCycleData();
    
    // TODO: Replace with fetch('/api/v1/dashboard') when Recommendation Engine is built
    return {
      profileName: mockProfile.name,
      cycle: cycleData,
      recentSymptomStatus: "Mild Acne, Moderate Fatigue",
      todayFocus: "Estrogen is rising. Great day for strength workouts and complex problem-solving.",
      tasks: [
        { id: "task1", text: "Drink Spearmint Tea (Morning/Evening)", completed: false },
        { id: "task2", text: "Strength Training (25 mins)", completed: true },
        { id: "task3", text: "Log Symptom: Acne/Bloating", completed: false }
      ]
    };
  },

  // ----------------------------------------------------
  // Symptom Logging
  // ----------------------------------------------------
  getSymptoms: async () => {
    // TODO: Replace with fetch('/api/v1/symptoms')
    return mockSymptoms;
  },

  logSymptom: async (log: Omit<SymptomLog, "date">) => {
    // TODO: Replace with fetch('/api/v1/symptoms', { method: 'POST', body: JSON.stringify(log) })
    const newLog: SymptomLog = {
      date: new Date().toISOString().split("T")[0],
      ...log
    };
    mockSymptoms = [newLog, ...mockSymptoms.filter(s => s.date !== newLog.date)];
    return newLog;
  },

  // ----------------------------------------------------
  // Cycle Data
  // ----------------------------------------------------
  getCycleData: async () => {
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      // We will send mock profile data to the engine for now,
      // this should eventually come from the user's actual saved state.
      const payload = {
        last_period_start_date: "2026-06-15",
        age: mockProfile.age,
        height: 165.0, // using default
        weight: 65.0,
        bmi: 23.9,
        previous_cycle_lengths: [30, 29, 31, 28, 30],
        pcos_diagnosed: true,
        sleep_hours: 6.5,
        stress_score: 5.0
      };
      
      const response = await fetch(`${baseUrl}/api/v1/pcos-cycle/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        throw new Error("Failed to fetch cycle data");
      }
      
      const data = await response.json();
      
      // Map backend response to frontend interface
      return {
        currentDay: data.cycle_day_today || 6,
        totalDays: data.predicted_cycle_length,
        phase: "Follicular", // Can be calculated based on currentDay vs ovulation_day_of_cycle
        phaseRemainingDays: data.days_until_next_period || 6, // Approximation for frontend display
        estrogen: 120, // default placeholder
        progesterone: 0.8, // default placeholder
        lh: 8.5, // default placeholder
        fsh: 6.2 // default placeholder
      } as CycleData;
      
    } catch (error) {
      console.error("Error calling Cycle Intelligence Engine:", error);
      // Fallback to mock data if backend isn't running
      return mockCycleData;
    }
  },

  // ----------------------------------------------------
  // Lab Analyzer
  // ----------------------------------------------------
  getLabMarkers: async () => {
    // TODO: Replace with fetch('/api/v1/labs')
    return mockLabMarkers;
  },

  uploadLabReport: async (file: File) => {
    // TODO: Replace with multipart form upload to fetch('/api/v1/labs/upload')
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          message: "Report parsed successfully",
          markers: mockLabMarkers
        });
      }, 1500); // Simulate upload latency
    });
  },

  // ----------------------------------------------------
  // AI Coach Chat
  // ----------------------------------------------------
  getCoachMessages: async () => {
    // TODO: Replace with fetch('/api/v1/coach/messages')
    return mockMessages;
  },

  sendMessageToCoach: async (text: string) => {
    // TODO: Replace with fetch('/api/v1/coach/messages', { method: 'POST', body: JSON.stringify({ text }) })
    const userMsg: CoachMessage = {
      id: String(mockMessages.length + 1),
      sender: "user",
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    mockMessages = [...mockMessages, userMsg];

    // Simulate AI reply
    return new Promise<CoachMessage>((resolve) => {
      setTimeout(() => {
        const coachMsg: CoachMessage = {
          id: String(mockMessages.length + 1),
          sender: "coach",
          text: `I've received your query about "${text}". As your coach, I recommend tracking this symptom daily. Would you like me to create a customized nutritional check-in plan for this?`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        mockMessages = [...mockMessages, coachMsg];
        resolve(coachMsg);
      }, 1200);
    });
  },

  // ----------------------------------------------------
  // Profile Data
  // ----------------------------------------------------
  getProfileData: async () => {
    // TODO: Replace with fetch('/api/v1/profile')
    return mockProfile;
  },

  updateProfileData: async (profile: Partial<ProfileData>) => {
    // TODO: Replace with fetch('/api/v1/profile', { method: 'PUT', body: JSON.stringify(profile) })
    mockProfile = {
      ...mockProfile,
      ...profile
    };
    return mockProfile;
  },

  // ----------------------------------------------------
  // Clinical Risk Engine
  // ----------------------------------------------------
  predictClinicalRisk: async (payload: any) => {
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${baseUrl}/api/v1/clinical-risk/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      return await response.json();
    } catch (error) {
      console.error("Error calling Clinical Risk Engine:", error);
      throw error;
    }
  }
};
