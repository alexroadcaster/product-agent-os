import type { Meta, StoryObj } from "@storybook/react";

type ButtonProps = {
  label: string;
  variant: "primary" | "danger";
};

function Button({ label, variant }: ButtonProps) {
  return <button data-variant={variant}>{label}</button>;
}

const meta = {
  title: "Synthetic/Button",
  component: Button,
  args: {
    label: "Continue",
    variant: "primary",
  },
} satisfies Meta<typeof Button>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Primary: Story = {};
export const Danger: Story = { args: { label: "Delete", variant: "danger" } };
