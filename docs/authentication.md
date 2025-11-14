# Authentication

This API uses JSON Web Tokens (JWT) for authentication. JWT is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object.

## How JWT Authentication Works

1. Client sends credentials (username/password) to the `/api/token/` endpoint
2. Server validates credentials and returns an access token and refresh token
3. Client includes the access token in the `Authorization` header for subsequent requests
4. When the access token expires, the client can use the refresh token to get a new access token

## Obtaining Tokens

### Request Access Token

```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### Successful Response

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Refreshing Tokens

When your access token expires, you can get a new one using the refresh token:

```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token_here"
}
```

## Using the Access Token

Include the access token in the `Authorization` header of your requests:

```
Authorization: Bearer your.access.token.here
```

## Token Expiration

- **Access Token**: 5 minutes (configurable)
- **Refresh Token**: 24 hours (configurable)

## Security Considerations

1. **Never expose your refresh token** in client-side code
2. **Always use HTTPS** in production
3. **Store tokens securely** - use HTTP-only cookies or secure storage
4. **Implement token rotation** - refresh tokens should be single-use
5. **Set appropriate token expiration times** based on your security requirements

## Example Authentication Flow

1. User logs in with username/password
2. Server returns access and refresh tokens
3. Client stores tokens securely
4. For each API request, include the access token in the Authorization header
5. When access token expires, use refresh token to get a new access token
6. If refresh token is expired or invalid, prompt user to log in again

## Error Responses

### Invalid Credentials (401)

```json
{
    "detail": "No active account found with the given credentials"
}
```

### Token Expired (401)

```json
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

### Missing Token (401)

```json
{
    "detail": "Authentication credentials were not provided."
}
```