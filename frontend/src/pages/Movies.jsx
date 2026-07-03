import { useEffect, useState } from "react";
import api from "../api/axios";

function Movies() {

    const [movies, setMovies] = useState([]);

    useEffect(() => {
        fetchMovies();
    }, []);

    const fetchMovies = async () => {

        try {

            const response = await api.get("/movies");

            setMovies(response.data);

        } catch (error) {

            console.log(error);

        }

    };

    return (

        <div>

            <h1>Movies</h1>

            {
                movies.map((movie) => (

                    <div key={movie.id}>

                        <h2>{movie.title}</h2>

                        <p>{movie.genre}</p>

                        <p>{movie.language}</p>

                        <p>{movie.durationMins} Minutes</p>

                        <hr />

                    </div>

                ))
            }

        </div>

    );

}

export default Movies;