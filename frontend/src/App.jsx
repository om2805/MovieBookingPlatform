import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Movies from "./pages/Movies";
import MovieDetail from "./pages/MovieDetail";
import SeatSelection from "./pages/SeatSelection";
import BookingHistory from "./pages/BookingHistory";

function App() {

    return (

        <Routes>

            <Route path="/" element={<Login />} />

            <Route path="/signup" element={<Signup />} />

            <Route path="/movies" element={<Movies />} />

            <Route path="/movie/:id" element={<MovieDetail />} />

            <Route path="/seats/:showId" element={<SeatSelection />} />

            <Route path="/bookings" element={<BookingHistory />} />

        </Routes>

    );

}

export default App;