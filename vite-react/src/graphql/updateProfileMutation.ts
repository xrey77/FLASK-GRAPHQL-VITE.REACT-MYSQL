import { gql } from '@apollo/client';

export const UPDATE_PROFILE = gql`
  mutation UpdateProfile($input: UserProfileInput!) {
    update_profile(input: $input) {
        message
    }
  }
`;

export interface UserData {
  id: number;
  firstname: string;
  lastname: string;
  email: string;
  mobile: string;
  username: string;
  isactivated: boolean;
  isblocked: boolean;
  mailtoken: string;
  userpic: string;
  qrcodeurl: string;
}

export interface ProfiledData {
  user: UserData;
}

export interface ProfileVariables {
  id: number;
  firstname: string;
  lastname: string;
  mobile: string;
}
