import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import DoctorDashboard from "./pages/DoctorDashboard";
import Interview from "./pages/Interview";
import Landing from "./pages/Landing";
import PatientHistory from "./pages/PatientHistory";
import PatientRegistration from "./pages/PatientRegistration";
import UploadReport from "./pages/UploadReport";
import "./styles/tokens.css";
import "./App.css";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/register" element={<PatientRegistration />} />
        <Route path="/interview/:patientId" element={<Interview />} />
        <Route path="/upload/:patientId" element={<UploadReport />} />
        <Route path="/history/:patientId" element={<PatientHistory />} />
        <Route path="/doctor" element={<DoctorDashboard />} />
        <Route path="/doctor/:patientId" element={<DoctorDashboard />} />
      </Routes>
    </Router>
  );
}
