from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import html


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "backend-complete-documentation.docx"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


DOCUMENT = """
# BookMyShow Backend Complete Documentation
Generated from the current working tree of the Spring Boot backend project.

# 1. Project Overview
This backend is a Java 17 Spring Boot application for a movie ticket booking system. It exposes REST APIs for authentication, movies, theaters, shows, users, and bookings. The application uses Spring MVC for HTTP APIs, Spring Data JPA for persistence, MySQL as the database, Spring Security with JWT for authentication and authorization, Jakarta Bean Validation for request validation, Lombok for boilerplate reduction, and Springdoc OpenAPI for Swagger UI.
The application entry point is org.example.bms.BmsApplication. Running this class starts the embedded server on port 8080 and loads all components under org.example.bms through Spring Boot component scanning.

# 2. Technology Stack
- Java 17: language level configured in pom.xml.
- Spring Boot 4.0.6: parent project and dependency management.
- Spring Web MVC: REST controllers and JSON request/response handling.
- Spring Data JPA and Hibernate: entity mapping and repository abstraction.
- MySQL Connector/J: runtime database driver.
- Spring Security: stateless authentication and role-based authorization.
- JJWT 0.12.5: JWT creation, signing, parsing, and validation.
- Jakarta Validation: @Valid, @NotBlank, @NotNull, @Positive, @Email, @Pattern, and @Size rules on DTOs.
- Lombok: @Data, @NoArgsConstructor, @AllArgsConstructor, and @RequiredArgsConstructor.
- Springdoc OpenAPI UI: Swagger UI under /swagger-ui/** and OpenAPI docs under /v3/api-docs/**.

# 3. Runtime Configuration
Configuration is stored in src/main/resources/application.properties.
- spring.application.name=bms identifies the Spring application.
- spring.datasource.url points to jdbc:mysql://localhost:3306/bms_db?createDatabaseIfNotExist=true.
- spring.datasource.username=root and spring.datasource.password=root are hardcoded development credentials.
- spring.jpa.hibernate.ddl-auto=update tells Hibernate to create or update tables from entity mappings at startup.
- spring.jpa.show-sql=true and spring.jpa.properties.hibernate.format_sql=true print formatted SQL in logs.
- server.port=8080 starts the HTTP server on port 8080.
- jwt.secret is the signing key for JWT tokens.
- jwt.expiration=86400000 gives tokens a 24 hour lifetime in milliseconds.

# 4. Package Structure
- org.example.bms: application entry point.
- configuration: Spring beans for password encoding, security filter chain, authentication manager, and CORS.
- controller: REST API controllers for auth, booking, movie, show, theater, and user operations.
- dto: request and response transfer objects. These define external API payloads and validation constraints.
- exceptiom: custom exceptions and global exception response handling. The package name appears to be misspelled as exceptiom.
- model: JPA entity classes and Role enum.
- repo: Spring Data repository interfaces.
- security: JWT filter and JWT service.
- service: business logic and DTO/entity mapping.

# 5. Application Startup Flow
- BmsApplication.main calls SpringApplication.run, which starts the Spring container and embedded web server.
- Spring scans org.example.bms and registers @Configuration, @Service, @Repository, @RestController, and @Component classes.
- AppConfig registers BCryptPasswordEncoder as the PasswordEncoder bean.
- SecurityConfig builds a stateless SecurityFilterChain and registers JwtAuthenticationFilter before UsernamePasswordAuthenticationFilter.
- JPA scans model classes and prepares database tables according to ddl-auto=update.
- Controllers become available under /api/... paths after startup.

# 6. Security and Authentication
Security is implemented with stateless JWT authentication. The backend does not create HTTP sessions because SessionCreationPolicy.STATELESS is configured.

## 6.1 Signup
POST /api/auth/signup accepts SignupRequestDto. AuthService.signup checks whether the email already exists, encodes the password with BCryptPasswordEncoder, assigns ROLE_USER, saves the User entity, and returns a success message.

## 6.2 Login
POST /api/auth/login accepts LoginRequestDto. AuthService.login delegates credential verification to AuthenticationManager using UsernamePasswordAuthenticationToken. If credentials are valid, JwtService.generateToken creates a signed token whose subject is the user email. The response body is AuthResponseDto containing the token string.

## 6.3 JWT Filter
JwtAuthenticationFilter extends OncePerRequestFilter. For each request, it reads the Authorization header. If the header starts with Bearer, it extracts the token, reads the email subject through JwtService.extractUsername, loads the user through CustomUserDetailsService, validates token signature and expiration, and places an authenticated UsernamePasswordAuthenticationToken in SecurityContextHolder.

## 6.4 User Details Loading
CustomUserDetailsService loads a User by email through UserRepository. It builds Spring Security UserDetails with username=email, password=encoded password, and roles from the Role enum after removing the ROLE_ prefix. ROLE_USER becomes USER internally.

## 6.5 Authorization Rules
- Public: /api/auth/**, /swagger-ui/**, and /v3/api-docs/**.
- Public read: GET /api/movies/**, GET /api/shows/**, and GET /api/theaters/**.
- Authenticated USER, MANAGER, or ADMIN: /api/users/me.
- ROLE_USER only: /api/bookings/**.
- ROLE_MANAGER or ROLE_ADMIN: POST, PUT, DELETE for /api/movies/**, /api/shows/**, and /api/theaters/**.
- ROLE_ADMIN only: /api/admin/** and /api/users/** except /api/users/me, which is matched earlier.

## 6.6 CORS
CORS allows requests from http://localhost:5173, permits all HTTP methods and headers, and allows credentials. This is designed for a frontend development server running on Vite default port 5173.

# 7. Domain Model and Database Entities
Entities are mapped with Jakarta Persistence annotations. Relationships use @ManyToOne, @OneToMany, and @OneToOne. Hibernate generates or updates the relational schema at startup.

## 7.1 User Entity
- Table: users.
- Fields: id, name, email, password, phoneNumber, role, active.
- email is unique and required. password is required and stores the BCrypt encoded password.
- role is stored as a string enum: ROLE_USER, ROLE_MANAGER, or ROLE_ADMIN.
- active defaults to true.
- Relationship: one user has many bookings through Booking.user.

## 7.2 Movie Entity
- Table: movies.
- Fields: id, title, description, language, genre, durationMins, releaseDate, posterUrl.
- Relationship: one movie has many shows through Show.movie.

## 7.3 Theater Entity
- Table: theaters.
- Fields: id, name, address, city, totalScreens.
- Relationship: one theater has many screens through Screen.theater.

## 7.4 Screen Entity
- Table: screens.
- Fields: id, name, totalSeats.
- Relationship: many screens belong to one theater.
- Relationship: one screen has many shows.
- Relationship: one screen has many seats.

## 7.5 Seat Entity
- Table: seats.
- Fields: id, seatNumber, seatType, basePrice.
- seatType is stored as a string such as GOLD, SILVER, or PLATINUM.
- Relationship: many seats belong to one screen.

## 7.6 Show Entity
- Table: shows.
- Fields: id, startTime, endTime.
- Relationship: many shows belong to one movie.
- Relationship: many shows belong to one screen.
- Relationship: one show has many show seats.
- Relationship: one show has many bookings.

## 7.7 ShowSeat Entity
- Table: show_seats.
- Fields: id, status, price.
- Relationship: many show seats belong to one show.
- Relationship: many show seats point to one base Seat.
- Relationship: many show seats may belong to one booking. booking_id is nullable before booking.
- status is expected to move across AVAILABLE, LOCKED, and BOOKED during booking, and back to AVAILABLE on cancellation.

## 7.8 Booking Entity
- Table: bookings.
- Fields: id, bookingNumber, bookingTime, status, totalAmount.
- bookingNumber is unique and generated with UUID.
- Relationship: many bookings belong to one user.
- Relationship: many bookings belong to one show.
- Relationship: one booking has many show seats.
- Relationship: one booking has one payment, cascaded with booking persistence.
- status is set to CONFIRMED during booking and CANCELLED during cancellation.

## 7.9 Payment Entity
- Table: payments.
- Fields: id, transactionId, amount, Status, paymentTime, paymentMethod.
- transactionId is unique and generated with UUID.
- Status stores payment state. The Java field name is capitalized as Status, but Lombok still creates getStatus and setStatus.
- Relationship: one payment is mapped by Booking.payment.

## 7.10 Role Enum
- ROLE_USER: normal customer role.
- ROLE_MANAGER: manager role allowed to manage movies, shows, and theaters.
- ROLE_ADMIN: admin role allowed manager operations and admin/user APIs.

# 8. DTO Layer
DTOs isolate API payloads from entity classes and control validation. Most mapping is manual inside service classes.

## 8.1 Authentication DTOs
- SignupRequestDto: name, email, password, phoneNumber. Validates nonblank name/email/password, email format, minimum password size 6, and exactly 10 digits phone number.
- LoginRequestDto: email and password. Validates email format and required password.
- AuthResponseDto: token. Returned by login.

## 8.2 UserDto
- Fields: id, name, email, phoneNumber.
- Used by UserController responses and nested booking responses. Password and role are intentionally not exposed.

## 8.3 MovieDto
- Fields: id, title, description, language, genre, durationMins, releaseDate, posterUrl.
- Used for movie create/read/update and nested show/booking responses.
- Validation requires title, description, language, genre, duration, release date, and poster URL. durationMins must be positive.

## 8.4 TheaterDto
- Fields: id, name, address, city, totalScreens.
- Validation requires name, address, city, and positive totalScreens.

## 8.5 ScreenDto
- Fields: id, name, totalSeats, theater.
- Used primarily inside ShowDto and BookingDto responses. There is no ScreenController in the current code.

## 8.6 SeatDto
- Fields: id, seatNumber, seatType, basePrice.
- Used inside ShowSeatDto to expose physical seat details.

## 8.7 ShowSeatDto
- Fields: id, seat, status, price.
- Used in ShowDto.availableSeats and BookingDto.seats.

## 8.8 ShowDto
- Fields: id, startTime, endTime, movie, screen, availableSeats.
- Validation requires startTime, endTime, movie, and screen.
- For show creation, only movie.id and screen.id are used by ShowService, together with startTime and endTime.

## 8.9 BookingRequestDto
- Fields: userId, showId, seatIds, paymentMethod.
- Validation requires userId, showId, at least one seat id, and payment method.

## 8.10 BookingDto
- Fields: id, bookingNumber, bookingTime, user, show, status, totalAmount, seats, payment.
- Returned after creating, reading, listing, or cancelling bookings.

## 8.11 PaymentDto
- Fields: id, transactionId, amount, paymentTime, paymentMethod, status.
- Embedded inside BookingDto when a booking has an associated payment.

# 9. Repository Layer
Repositories extend JpaRepository and rely on Spring Data derived query methods. ShowSeatRepository also defines a pessimistic locking query for safe booking.
- UserRepository: findByEmail and existsByEmail.
- MovieRepository: findByLanguage, findByGenre, and findByTitleContaining.
- TheaterRepository: findByCity.
- ScreenRepository: findByTheaterId.
- ShowRepository: findByMovieId, findByScreenId, findByStartTimeBetween, and findByMovie_IdAndScreen_Theater_City.
- ShowSeatRepository: findSeatsForUpdate uses @Lock(PESSIMISTIC_WRITE) to lock selected rows by ids, findByBooking_Id fetches booked seats for a booking, and findByShowIdAndStatus fetches available seats for show responses.
- BookingRepository: findByUserId, findByBookingNumber, and findByShowId.
- PaymentRepository: findByTransactionId.

# 10. Service Layer
## 10.1 AuthService
AuthService handles signup and login. Signup performs duplicate email detection, password hashing, user creation, role assignment, and persistence. Login authenticates credentials through AuthenticationManager and returns a JWT token through JwtService.

## 10.2 CustomUserDetailsService
This service adapts application users to Spring Security UserDetails. It is used during login authentication and JWT request authentication.

## 10.3 UserService
UserService fetches, updates, deletes, and maps users. It supports lookup by id and email. updateUser changes name, email, and phone number. deleteUser physically deletes the user from the database.

## 10.4 MovieService
MovieService creates, reads, updates, deletes, and maps movies. It contains helper methods for language, genre, and title search. In the current controller, only createMovie, getMovieById, and getAllMovies are exposed through HTTP.

## 10.5 TheaterService
TheaterService creates, reads, lists, filters by city, updates, deletes, and maps theaters. It does not manage nested screens or seats directly.

## 10.6 ShowService
ShowService creates and reads shows. To create a show, it loads Movie by showDto.movie.id and Screen by showDto.screen.id, sets start/end time, and saves a Show. Read methods fetch available seats by show id and status AVAILABLE and include them in ShowDto.availableSeats.
Important behavior: createShow currently does not create ShowSeat rows for the screen seats. It only saves the Show and then queries for existing AVAILABLE show seats. Show seats must be inserted by another process or manually in the database for availability and booking to work.

## 10.7 BookingService
BookingService contains the critical booking workflow. createBooking is @Transactional and uses pessimistic row locks to prevent two concurrent requests from booking the same seats.
- Step 1: Load User by bookingRequest.userId. If missing, throw ResourceNotFoundException.
- Step 2: Load Show by bookingRequest.showId. If missing, throw ResourceNotFoundException.
- Step 3: Lock requested ShowSeat rows using ShowSeatRepository.findSeatsForUpdate. The query uses PESSIMISTIC_WRITE.
- Step 4: Verify the number of locked seats equals the number requested.
- Step 5: Verify each ShowSeat belongs to the selected Show.
- Step 6: Verify each ShowSeat has status AVAILABLE. If not, throw SeatUnavailableException.
- Step 7: Mark selected seats as LOCKED and save them.
- Step 8: Compute totalAmount by summing ShowSeat.price.
- Step 9: Create a Payment with amount, current payment time, supplied payment method, status SUCCESS, and generated transaction UUID.
- Step 10: Create Booking with user, show, current booking time, status CONFIRMED, total amount, generated booking UUID, and payment.
- Step 11: Save Booking. Because Booking.payment has cascade ALL, Payment is saved with the booking.
- Step 12: Change selected seats to BOOKED and attach them to the saved Booking.
- Step 13: Save ShowSeat rows and return a fully nested BookingDto.
cancelBooking is @Transactional. It loads the booking, checks that the authenticated email matches booking.user.email, sets booking status to CANCELLED, releases associated ShowSeat rows back to AVAILABLE, removes their booking link, changes payment status to REFUNDED when present, saves booking and seats, and returns the updated BookingDto.
getMyBookings resolves the authenticated user by email, fetches bookings by user id, loads each booking seats, and maps each booking to BookingDto.
getBookingById loads a booking by id and maps it with its associated ShowSeat rows. It does not currently enforce ownership in the service.

# 11. REST API Documentation
## 11.1 Authentication APIs
- POST /api/auth/signup: public. Request SignupRequestDto. Creates a ROLE_USER account. Response is plain string: User Registered Successfully.
- POST /api/auth/login: public. Request LoginRequestDto. Authenticates credentials and returns AuthResponseDto containing token.

## 11.2 Movie APIs
- POST /api/movies: manager/admin. Request MovieDto. Creates a movie and returns created MovieDto with HTTP 201.
- GET /api/movies/{id}: public. Returns MovieDto by id.
- GET /api/movies: public. Returns all movies.
SecurityConfig defines PUT and DELETE permissions for /api/movies/**, and MovieService has update/delete methods, but MoviesController currently exposes no PUT or DELETE endpoints.

## 11.3 Theater APIs
- POST /api/theaters: manager/admin. Request TheaterDto. Creates a theater and returns HTTP 201.
- GET /api/theaters/{theaterId}: public. Returns one theater by id.
- GET /api/theaters: public. Returns all theaters.
- GET /api/theaters/city/{city}: public. Returns theaters by city.
- PUT /api/theaters/{theaterId}: manager/admin. Updates name, address, city, and totalScreens.
- DELETE /api/theaters/{theaterId}: manager/admin. Deletes the theater and returns the deleted TheaterDto.

## 11.4 Show APIs
- POST /api/shows: manager/admin. Request ShowDto. Creates a show and returns ShowDto with HTTP 201.
- GET /api/shows: public. Returns all shows with available seats.
- GET /api/shows/{id}: public. Returns one show by id with available seats.
- GET /api/shows/movie/{movieId}: public. Returns shows for a movie.
- GET /api/shows/movie/{movieId}/city/{city}: public. Returns shows for a movie in a city.
- GET /api/shows/date-range?startDate=...&endDate=...: public. Dates must be ISO date-time format.
SecurityConfig defines PUT and DELETE permissions for /api/shows/**, but ShowController currently exposes no PUT or DELETE endpoints.

## 11.5 Booking APIs
- POST /api/bookings: ROLE_USER. Request BookingRequestDto. Creates booking, payment, and booked show seats. Returns BookingDto with HTTP 201.
- GET /api/bookings/{id}: ROLE_USER. Returns booking by id.
- GET /api/bookings/my-bookings: ROLE_USER. Reads authenticated email from SecurityContextHolder and returns bookings for that user.
- DELETE /api/bookings/{bookingId}: ROLE_USER. Cancels authenticated user booking and releases seats.
Important security note: createBooking accepts userId in the request body and does not compare it with the authenticated user email. A ROLE_USER could send another userId unless additional checks are added.

## 11.6 User APIs
- GET /api/users/me: ROLE_USER, ROLE_MANAGER, or ROLE_ADMIN. Returns the currently authenticated user based on JWT subject email.
- GET /api/users/{userId}: ROLE_ADMIN. Returns a user by id.
- PUT /api/users/{userId}: ROLE_ADMIN. Updates user name, email, and phone number.
- DELETE /api/users/{userId}: ROLE_ADMIN. Deletes a user and returns deleted UserDto.

# 12. Error Handling
GlobalExceptionHandler is annotated with @ControllerAdvice and converts exceptions into ErrorResponse objects with timestamp, error, message, status, and path.
- ResourceNotFoundException returns HTTP 404 with error not Found.
- SeatUnavailableException returns HTTP 400 with error Bad Request.
- BadCredentialsException returns HTTP 401 with message Invalid email or password.
- AccessDeniedException returns HTTP 403 with message Access Denied.
- Any other Exception returns HTTP 500 with error Server Error and the exception message.
Validation errors from @Valid are not handled explicitly in GlobalExceptionHandler, so Spring default validation handling applies.

# 13. Booking Concurrency
The booking flow is designed to prevent double-booking seats. The core protection is ShowSeatRepository.findSeatsForUpdate, annotated with @Lock(LockModeType.PESSIMISTIC_WRITE). Since BookingService.createBooking is transactional, the lock is held until the transaction completes. If two users try to book the same ShowSeat row, only one transaction should see it as AVAILABLE first. The successful transaction changes it to BOOKED. The other transaction should eventually see a non-AVAILABLE status and fail with SeatUnavailableException.
BookingConcurrencyTest starts two concurrent tasks that both attempt to book userId=1, showId=1, and seatId=1 with payment method UPI. It expects one success and one failure. This test depends on database seed data already existing with those ids and with the seat initially AVAILABLE.

# 14. Data Flow Examples
## 14.1 Login Flow
- Client sends POST /api/auth/login with email and password.
- AuthController calls AuthService.login.
- AuthenticationManager uses CustomUserDetailsService to load the user by email and verify BCrypt password.
- JwtService generates token with subject=email and configured expiration.
- Client stores token and sends it in Authorization: Bearer <token> for protected APIs.

## 14.2 Protected Request Flow
- Client sends request with Authorization header.
- JwtAuthenticationFilter extracts and validates token.
- CustomUserDetailsService loads authorities from database role.
- SecurityContextHolder receives authenticated principal.
- SecurityConfig authorization rules decide whether the endpoint is allowed.
- Controller reads current email from SecurityContextHolder when needed, for example /api/users/me or /api/bookings/my-bookings.

## 14.3 Booking Flow
- Client sends POST /api/bookings with userId, showId, seatIds, and paymentMethod.
- BookingController validates the DTO and calls BookingService.createBooking.
- BookingService locks requested show seats, validates ownership and availability, creates payment and booking records, marks seats BOOKED, and returns BookingDto.

## 14.4 Cancellation Flow
- Client sends DELETE /api/bookings/{bookingId} with JWT.
- BookingController reads authenticated email and calls BookingService.cancelBooking.
- BookingService checks booking ownership, marks booking CANCELLED, releases seats to AVAILABLE, marks payment REFUNDED, and returns BookingDto.

# 15. Current Implementation Observations
- The package name exceptiom is likely a typo and could be renamed to exception with import updates.
- application.properties contains hardcoded database credentials and JWT secret.
- MoviesController does not expose update/delete endpoints although MovieService and SecurityConfig suggest they are intended.
- ShowController does not expose update/delete endpoints although SecurityConfig includes manager/admin rules for them.
- MovieService.getMovieByGenre currently calls movieRepository.findByLanguage(genre) instead of findByGenre(genre).
- MovieService.searchMovies currently calls movieRepository.findByLanguage(title) instead of findByTitleContaining(title).
- ShowService.createShow does not create ShowSeat rows for seats on the selected screen. Booking requires ShowSeat rows to already exist.
- BookingService.createBooking trusts userId from request body instead of forcing the authenticated user.
- GET /api/bookings/{id} returns a booking by id for any ROLE_USER and does not check booking ownership.
- The concurrency test depends on pre-existing database records with fixed ids, so it is not isolated or repeatable on an empty database.
- Payment field Status starts with uppercase letter, which is unusual Java style.

# 16. How To Run Locally
- Install Java 17 and Maven or use the included Maven wrapper.
- Start MySQL locally and ensure root/root credentials work, or update application.properties.
- Run: .\\mvnw.cmd spring-boot:run
- API base URL: http://localhost:8080
- Swagger UI: http://localhost:8080/swagger-ui/index.html
- Frontend CORS origin currently allowed: http://localhost:5173

# 17. Test Coverage
- BmsApplicationTests.contextLoads verifies that the Spring application context can start.
- BookingConcurrencyTest verifies pessimistic locking behavior for the same show seat under two concurrent booking attempts, assuming fixed seed data exists.
- There are no controller slice tests, repository tests with isolated data setup, authentication tests, authorization tests, or validation error tests in the current source tree.

# 18. Full Backend Source Code Appendix
This appendix is generated from the current files in the workspace. It includes pom.xml, runtime properties, all Java source files under src/main/java/org/example/bms, and backend tests under src/test/java/org/example/bms.
"""


def xml_escape(value: str) -> str:
    return html.escape(value, quote=False)


class DocxBuilder:
    def __init__(self) -> None:
        self.body: list[str] = []

    def paragraph(self, text: str = "", style: str | None = None) -> None:
        style_xml = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        runs = []
        for index, part in enumerate(text.split("\n")):
            if index:
                runs.append("<w:r><w:br/></w:r>")
            runs.append(f'<w:r><w:t xml:space="preserve">{xml_escape(part)}</w:t></w:r>')
        self.body.append(f"<w:p>{style_xml}{''.join(runs)}</w:p>")

    def code_line(self, text: str) -> None:
        self.body.append(
            '<w:p><w:pPr><w:pStyle w:val="CodeBlock"/></w:pPr>'
            '<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="17"/></w:rPr>'
            f'<w:t xml:space="preserve">{xml_escape(text)}</w:t></w:r></w:p>'
        )

    def page_break(self) -> None:
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def add_markdownish(self, text: str) -> None:
        for raw_line in text.strip().splitlines():
            line = raw_line.rstrip()
            if not line:
                continue
            if line.startswith("# "):
                if self.body:
                    self.page_break()
                self.paragraph(line[2:], "Heading1")
            elif line.startswith("## "):
                self.paragraph(line[3:], "Heading2")
            elif line.startswith("- "):
                self.paragraph(line, "ListParagraph")
            else:
                self.paragraph(line)

    def add_source_appendix(self, paths: list[Path]) -> None:
        for path in paths:
            rel = path.relative_to(ROOT).as_posix()
            self.page_break()
            self.paragraph(rel, "Heading2")
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = path.read_text(encoding="cp1252")
            for line in text.splitlines():
                self.code_line(line)

    def document_xml(self) -> str:
        self.body.append(
            '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
            '<w:pgMar w:top="1008" w:right="1008" w:bottom="1008" w:left="1008" '
            'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
        )
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document xmlns:w="{WORD_NS}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f"<w:body>{''.join(self.body)}</w:body></w:document>"
        )


def styles_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{WORD_NS}">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:after="160" w:line="276" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="360" w:after="180"/></w:pPr>
    <w:rPr><w:b/><w:color w:val="1F4E79"/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="260" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:color w:val="2F5496"/><w:sz w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph">
    <w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:ind w:left="360" w:hanging="240"/><w:spacing w:after="80"/></w:pPr>
    <w:rPr><w:sz w:val="21"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="CodeBlock">
    <w:name w:val="Code Block"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="0" w:after="0" w:line="220" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="17"/></w:rPr>
  </w:style>
</w:styles>
"""


def collect_sources() -> list[Path]:
    paths: list[Path] = []
    for pattern in (
        "pom.xml",
        "src/main/resources/application.properties",
        "src/main/java/org/example/bms/**/*.java",
        "src/test/java/org/example/bms/**/*.java",
    ):
        paths.extend(sorted(ROOT.glob(pattern)))
    return [path for path in paths if path.is_file()]


def write_docx(document_xml: str) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""
    word_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""
    core = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>BookMyShow Backend Complete Documentation</dc:title>
  <dc:subject>Backend architecture and full source documentation</dc:subject>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""
    app = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>Codex OOXML Generator</Application>
</Properties>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUT, "w", ZIP_DEFLATED) as zip_file:
        zip_file.writestr("[Content_Types].xml", content_types)
        zip_file.writestr("_rels/.rels", rels)
        zip_file.writestr("word/_rels/document.xml.rels", word_rels)
        zip_file.writestr("word/document.xml", document_xml)
        zip_file.writestr("word/styles.xml", styles_xml())
        zip_file.writestr("docProps/core.xml", core)
        zip_file.writestr("docProps/app.xml", app)


def main() -> None:
    sources = collect_sources()
    builder = DocxBuilder()
    builder.add_markdownish(DOCUMENT)
    builder.add_source_appendix(sources)
    write_docx(builder.document_xml())
    print(OUT)
    print(f"Included {len(sources)} source/config/test files")
    print(f"Size bytes: {OUT.stat().st_size}")


if __name__ == "__main__":
    main()
