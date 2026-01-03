return {
  -- add gruvbox
  { "RRethy/nvim-base16" },

  -- Configure LazyVim to load gruvbox
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "base16-grayscale-dark",
    },
  },
}
