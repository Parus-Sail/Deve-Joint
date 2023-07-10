class RequestFormKwargsMixin:
    """
    Передаем request в форму.
    CBV mixin which puts the request into the form kwargs.
    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self):
        kwargs = super(RequestFormKwargsMixin, self).get_form_kwargs()

        # Update the existing form kwargs dict with the request's user.
        kwargs.update({"request": self.request})
        return kwargs
