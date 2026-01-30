//src/api/auth.ts
import axiosClient from "../axiosClient";

export interface AuthCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
}

const authApi = {
  login: async (credentials: AuthCredentials): Promise<AuthResponse> => {
    const response = await axiosClient.post<AuthResponse>(
      "/auth/login",
      credentials
    );
    return response.data;
  },

  register: async (credentials: AuthCredentials): Promise<AuthResponse> => {
    const response = await axiosClient.post<AuthResponse>(
      "/auth/register",
      credentials
    );
    return response.data;
  },
};

export default authApi;
