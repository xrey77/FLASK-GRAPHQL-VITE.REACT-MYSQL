import { gql } from '@apollo/client';

export const CHANGE_PASSWORD = gql`
  mutation ChangePassword($input: PasswordInput!) {
    change_password(input: $input) {
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

export interface PasswordData {
  user: UserData;
}

export interface PasswordVariables {
  id: number;
  password: string;
}
